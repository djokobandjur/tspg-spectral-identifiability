from __future__ import annotations
from contextlib import contextmanager
import math
import numpy as np
import torch
import torch.nn.functional as F

@contextmanager
def math_sdpa_context():
    try:
        from torch.nn.attention import sdpa_kernel, SDPBackend
        with sdpa_kernel(backends=[SDPBackend.MATH]):
            yield
        return
    except Exception:
        pass
    with torch.backends.cuda.sdp_kernel(
        enable_flash=False, enable_math=True, enable_mem_efficient=False, enable_cudnn=False
    ):
        yield

def native_spec(model, family):
    if family == "learned":
        shape = tuple(model.pos_encoding.pos_embed.shape)
        return {"shape": shape, "d": int(model.pos_encoding.pos_embed.numel())}
    if family == "sinusoidal":
        shape = tuple(model.pos_encoding.pe.shape)
        return {"shape": shape, "d": int(model.pos_encoding.pe.numel())}
    if family == "rope":
        ref = model.blocks[0].attn.rope.cos_cached
        shape = tuple(ref.shape)
        return {"shape": shape, "d": int(ref.numel())}
    if family == "alibi":
        ref = model.blocks[0].attn.alibi.slopes
        shape = tuple(ref.shape)
        return {"shape": shape, "d": int(ref.numel())}
    raise ValueError(family)

def zeros_native(model, family, device=None):
    spec = native_spec(model, family)
    dev = device or next(model.parameters()).device
    return torch.zeros(spec["d"], device=dev, dtype=torch.float32)

def _reshape_delta(model, family, delta):
    return delta.reshape(native_spec(model, family)["shape"])

def _rotate_half(x):
    x1, x2 = x[..., :x.shape[-1]//2], x[..., x.shape[-1]//2:]
    return torch.cat((-x2, x1), dim=-1)

def forward_with_native_delta(model, images, delta, family, backend="canonical", return_centered_logits=False):
    B = images.shape[0]
    dsh = _reshape_delta(model, family, delta)

    x = model.patch_embed(images)
    cls = model.cls_token.expand(B, -1, -1)
    x = torch.cat([cls, x], dim=1)

    if family == "learned":
        x = x + model.pos_encoding.pos_embed + dsh
    elif family == "sinusoidal":
        x = x + model.pos_encoding.pe + dsh
    elif family in ("rope", "alibi"):
        pass
    else:
        raise ValueError(family)

    centered = []
    ctx = math_sdpa_context() if backend == "math" else None
    if ctx is not None:
        ctx.__enter__()
    try:
        for block in model.blocks:
            y = block.norm1(x)
            attn = block.attn
            bsz, n_tokens, channels = y.shape
            qkv = attn.qkv(y).reshape(
                bsz, n_tokens, 3, attn.num_heads, attn.head_dim
            ).permute(2,0,3,1,4)
            q,k,v = qkv[0],qkv[1],qkv[2]

            attn_bias = None
            if family == "rope":
                base_cos = attn.rope.cos_cached[:, :, :n_tokens, :]
                base_sin = attn.rope.sin_cached[:, :, :n_tokens, :]
                dd = dsh[:, :, :n_tokens, :]
                cd, sd = torch.cos(dd), torch.sin(dd)
                cos_half = base_cos * cd - base_sin * sd
                sin_half = base_sin * cd + base_cos * sd
                cos = torch.cat([cos_half, cos_half], dim=-1)
                sin = torch.cat([sin_half, sin_half], dim=-1)
                q = q * cos + _rotate_half(q) * sin
                k = k * cos + _rotate_half(k) * sin
            elif family == "alibi":
                base = attn.alibi.slopes
                dist = attn.alibi.rel_dist[:, :, :n_tokens, :n_tokens]
                attn_bias = -(base + dsh) * dist

            z = (q @ k.transpose(-2,-1)) * attn.scale
            if attn_bias is not None:
                z = z + attn_bias
            if return_centered_logits:
                centered.append(z - z.mean(dim=-1, keepdim=True))

            out = F.scaled_dot_product_attention(
                q,k,v,attn_mask=attn_bias,dropout_p=0.0
            )
            out = out.transpose(1,2).reshape(bsz,n_tokens,channels)
            out = attn.proj(out)
            x = x + out
            x = x + block.mlp(block.norm2(x))
    finally:
        if ctx is not None:
            ctx.__exit__(None,None,None)

    x = model.norm(x)
    logits = model.head(x[:,0])
    return (logits, tuple(centered)) if return_centered_logits else logits

def per_example_losses_and_grads(model, images, labels, family, prefer_batched=True):
    delta = zeros_native(model, family, images.device).requires_grad_(True)
    logits = forward_with_native_delta(model, images, delta, family, backend="math")
    losses = F.cross_entropy(logits, labels, reduction="none")
    B = losses.shape[0]

    if prefer_batched:
        eye = torch.eye(B, device=losses.device, dtype=losses.dtype)
        try:
            g = torch.autograd.grad(
                losses, delta, grad_outputs=eye,
                is_grads_batched=True, retain_graph=False, create_graph=False
            )[0]
            return logits.detach(), losses.detach(), g.detach(), "batched_vjp_math_sdpa"
        except Exception:
            pass

    rows = []
    for i in range(B):
        di = zeros_native(model, family, images.device).requires_grad_(True)
        li = F.cross_entropy(
            forward_with_native_delta(model, images[i:i+1], di, family, backend="math"),
            labels[i:i+1], reduction="sum"
        )
        gi = torch.autograd.grad(li, di)[0]
        rows.append(gi.detach())
    return logits.detach(), losses.detach(), torch.stack(rows), "loop_vjp_math_sdpa"

def compare_batched_loop(model, images, labels, family):
    _, Lb, Gb, mb = per_example_losses_and_grads(model, images, labels, family, True)
    _, Ll, Gl, ml = per_example_losses_and_grads(model, images, labels, family, False)
    diff = Gb.double() - Gl.double()
    rel = float(torch.linalg.vector_norm(diff) / max(torch.linalg.vector_norm(Gl.double()), torch.tensor(1e-30, device=Gl.device)))
    return {
        "preferred_method":mb, "reference_method":ml,
        "loss_max_abs":float((Lb-Ll).abs().max().item()),
        "grad_max_abs":float(diff.abs().max().item()),
        "grad_relative_l2":rel,
    }

def mean_gradient_identity(model, images, labels, family, per_grads):
    delta = zeros_native(model, family, images.device).requires_grad_(True)
    losses = F.cross_entropy(
        forward_with_native_delta(model, images, delta, family, backend="math"),
        labels, reduction="none"
    )
    gmean = torch.autograd.grad(losses.mean(), delta)[0].detach().double()
    ref = per_grads.double().mean(dim=0)
    rel = float(torch.linalg.vector_norm(gmean-ref) / max(torch.linalg.vector_norm(ref), torch.tensor(1e-30, device=ref.device)))
    return {"relative_l2_error":rel, "max_abs_error":float((gmean-ref).abs().max().item())}

def rope_unit_circle_error(model):
    errs=[]
    share_cos=[]
    share_sin=[]
    c0=model.blocks[0].attn.rope.cos_cached
    s0=model.blocks[0].attn.rope.sin_cached
    for b in model.blocks:
        c=b.attn.rope.cos_cached
        s=b.attn.rope.sin_cached
        errs.append(float((c.square()+s.square()-1.0).abs().max().item()))
        share_cos.append(float((c-c0).abs().max().item()))
        share_sin.append(float((s-s0).abs().max().item()))
    return {
        "unit_circle_max_abs_error":max(errs),
        "cross_block_cos_max_abs":max(share_cos),
        "cross_block_sin_max_abs":max(share_sin),
    }

def deterministic_native_direction(model, family, seed):
    d=native_spec(model,family)["d"]
    rng=np.random.default_rng(int(seed))
    v=rng.integers(0,2,size=d,dtype=np.int8).astype(np.float32)
    v=2.0*v-1.0
    return torch.from_numpy(v).to(next(model.parameters()).device)

def attention_jvp_quadratic(model, image, family, direction):
    zero=zeros_native(model,family,image.device)
    def fn(delta):
        _, zs = forward_with_native_delta(
            model, image, delta, family, backend="math", return_centered_logits=True
        )
        return zs

    clean, tangents = torch.func.jvp(fn, (zero,), (direction,))
    clean_energy = sum(z.double().square().sum() for z in clean)
    tangent_energy = sum(t.double().square().sum() for t in tangents)
    q=float((tangent_energy / clean_energy).item())
    finite=bool(torch.isfinite(torch.tensor(q)))
    return {
        "centered_clean_energy":float(clean_energy.item()),
        "centered_jvp_energy":float(tangent_energy.item()),
        "normalized_quadratic_response":q,
        "finite":finite,
        "positive":bool(q>0),
        "layer_count":len(clean),
    }
