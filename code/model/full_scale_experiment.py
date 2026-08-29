#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Full-Scale Positional Encoding Analysis for Vision Transformers
=============================================================================

Quantifying the Information Content of Positional Encoding in ViT:
Learned vs. Sinusoidal vs. RoPE vs. ALiBi

Dataset:    ImageNet-100 (100 classes, 224x224, ~130K train / ~5K val)
Model:      ViT-Base (12 layers, 768 dim, 12 heads, patch 16x16 → 196 patches)
Seeds:      3 independent runs per configuration
PE types:   Sinusoidal, Learned, RoPE, ALiBi

Requirements:
    pip install torch torchvision timm matplotlib numpy scipy scikit-learn tqdm

Hardware:   1x H100/A100 GPU 
           
Usage:
    python full_scale_experiment.py --data_dir /path/to/imagenet100 --output_dir ./results

    python full_scale_experiment.py --data_dir /path/to/imagenet100 --mode train --pe_type learned --seed 42
=============================================================================
"""

import os
import io
import json
import argparse
import math
import time
from pathlib import Path
from collections import OrderedDict

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
from tqdm import tqdm

# ============================================================================
# 1. MODEL DEFINITIONS
# ============================================================================

class PatchEmbedding(nn.Module):
    """Convert image to patch embeddings."""
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        self.num_patches = (img_size // patch_size) ** 2
        self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        # x: (B, C, H, W) -> (B, num_patches, embed_dim)
        return self.proj(x).flatten(2).transpose(1, 2)


# --- Positional Encoding Variants ---

class LearnedPE(nn.Module):
    """Learnable positional encoding."""
    def __init__(self, num_positions, embed_dim):
        super().__init__()
        self.pos_embed = nn.Parameter(torch.randn(1, num_positions, embed_dim) * 0.02)

    def forward(self, x):
        return x + self.pos_embed


class SinusoidalPE(nn.Module):
    """Fixed sinusoidal positional encoding (Vaswani et al., 2017)."""
    def __init__(self, num_positions, embed_dim):
        super().__init__()
        pe = torch.zeros(num_positions, embed_dim)
        position = torch.arange(0, num_positions, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))  # (1, num_positions, embed_dim)

    def forward(self, x):
        return x + self.pe


class RoPE(nn.Module):
    """Rotary Position Embedding (Su et al., 2021).

    Applied within the attention mechanism, not as additive PE.
    Returns position-encoded Q and K inside the attention block.
    """
    def __init__(self, num_positions, head_dim):
        super().__init__()
        # Precompute rotation frequencies
        inv_freq = 1.0 / (10000 ** (torch.arange(0, head_dim, 2).float() / head_dim))
        self.register_buffer('inv_freq', inv_freq)

        # Precompute sin/cos for all positions
        t = torch.arange(num_positions, dtype=torch.float)
        freqs = torch.einsum('i,j->ij', t, inv_freq)  # (num_positions, head_dim/2)
        self.register_buffer('cos_cached', freqs.cos().unsqueeze(0).unsqueeze(0))  # (1, 1, N, D/2)
        self.register_buffer('sin_cached', freqs.sin().unsqueeze(0).unsqueeze(0))

    def _rotate_half(self, x):
        """Split x into two halves and rotate."""
        x1, x2 = x[..., :x.shape[-1]//2], x[..., x.shape[-1]//2:]
        return torch.cat((-x2, x1), dim=-1)

    def forward(self, q, k, seq_len):
        """Apply rotary embeddings to Q and K.
        q, k: (B, num_heads, seq_len, head_dim)
        """
        cos = self.cos_cached[:, :, :seq_len, :]  # (1, 1, seq_len, D/2)
        sin = self.sin_cached[:, :, :seq_len, :]

        # Expand cos/sin to match head_dim (repeat for both halves)
        cos = torch.cat([cos, cos], dim=-1)  # (1, 1, seq_len, D)
        sin = torch.cat([sin, sin], dim=-1)

        q_rot = q * cos + self._rotate_half(q) * sin
        k_rot = k * cos + self._rotate_half(k) * sin
        return q_rot, k_rot


class ALiBi(nn.Module):
    """Attention with Linear Biases (Press et al., 2022).

    Adds a linear bias to attention scores based on relative distance.
    No positional embedding is added to the input.
    """
    def __init__(self, num_heads, num_positions):
        super().__init__()
        # Compute slopes for attention heads (following ALiBi paper)
        def get_slopes(n):
            def get_slopes_power_of_2(n):
                start = (2**(-2**-(math.log2(n)-3)))
                ratio = start
                return [start*ratio**i for i in range(n)]
            if math.log2(n).is_integer():
                return get_slopes_power_of_2(n)
            else:
                closest_power_of_2 = 2**math.floor(math.log2(n))
                return get_slopes_power_of_2(closest_power_of_2) + \
                       get_slopes(2*closest_power_of_2)[0::2][:n-closest_power_of_2]

        slopes = torch.tensor(get_slopes(num_heads)).view(1, num_heads, 1, 1)
        self.register_buffer('slopes', slopes)

        # Compute relative position bias matrix
        positions = torch.arange(num_positions)
        relative_positions = positions.unsqueeze(0) - positions.unsqueeze(1)
        relative_positions = -torch.abs(relative_positions).float()
        self.register_buffer('relative_positions', relative_positions.unsqueeze(0).unsqueeze(0))

    def forward(self, attn_scores, seq_len):
        """Add ALiBi bias to attention scores.
        attn_scores: (B, num_heads, seq_len, seq_len)
        """
        bias = self.slopes * self.relative_positions[:, :, :seq_len, :seq_len]
        return attn_scores + bias


class MultiHeadAttention(nn.Module):
    """Multi-head self-attention with optional RoPE or ALiBi."""
    def __init__(self, embed_dim=768, num_heads=12, pe_type='learned', num_positions=197, dropout=0.0):
        super().__init__()
        assert embed_dim % num_heads == 0
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale = self.head_dim ** -0.5
        self.pe_type = pe_type.lower()

        self.qkv = nn.Linear(embed_dim, embed_dim * 3)
        self.proj = nn.Linear(embed_dim, embed_dim)
        self.attn_drop = nn.Dropout(dropout)
        self.proj_drop = nn.Dropout(dropout)

        if self.pe_type == 'rope':
            self.rope = RoPE(num_positions, self.head_dim)
        elif self.pe_type == 'alibi':
            self.alibi = ALiBi(num_heads, num_positions)

    def forward(self, x, return_attention=False):
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        if self.pe_type == 'rope':
            q, k = self.rope(q, k, N)

        attn = (q @ k.transpose(-2, -1)) * self.scale

        if self.pe_type == 'alibi':
            attn = self.alibi(attn, N)

        attn = attn.softmax(dim=-1)
        attn_weights = attn if return_attention else None
        attn = self.attn_drop(attn)

        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        x = self.proj(x)
        x = self.proj_drop(x)
        return x, attn_weights


class MLP(nn.Module):
    def __init__(self, in_features, hidden_features=None, out_features=None, dropout=0.0):
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = nn.GELU()
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(dropout)

    def forward(self, x):
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x


class TransformerBlock(nn.Module):
    def __init__(self, embed_dim=768, num_heads=12, mlp_ratio=4.0, pe_type='learned', num_positions=197, dropout=0.0):
        super().__init__()
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = MultiHeadAttention(embed_dim, num_heads, pe_type, num_positions, dropout)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.mlp = MLP(embed_dim, int(embed_dim * mlp_ratio), dropout=dropout)

    def forward(self, x, return_attention=False):
        attn_out, attn_weights = self.attn(self.norm1(x), return_attention)
        x = x + attn_out
        x = x + self.mlp(self.norm2(x))
        return x, attn_weights


class VisionTransformer(nn.Module):
    """Vision Transformer with configurable positional encoding."""
    def __init__(self, img_size=224, patch_size=16, in_channels=3, num_classes=100,
                 embed_dim=768, depth=12, num_heads=12, mlp_ratio=4.0,
                 pe_type='learned', dropout=0.0):
        super().__init__()
        self.num_classes = num_classes
        self.embed_dim = embed_dim
        self.pe_type = pe_type.lower()

        self.patch_embed = PatchEmbedding(img_size, patch_size, in_channels, embed_dim)
        num_patches = self.patch_embed.num_patches
        num_positions = num_patches + 1  # +1 for CLS token

        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))

        if self.pe_type == 'learned':
            self.pos_embed = LearnedPE(num_positions, embed_dim)
        elif self.pe_type == 'sinusoidal':
            self.pos_embed = SinusoidalPE(num_positions, embed_dim)
        else:
            self.pos_embed = None

        self.pos_drop = nn.Dropout(dropout)

        self.blocks = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads, mlp_ratio, self.pe_type, num_positions, dropout)
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)

        self._init_weights()

    def _init_weights(self):
        nn.init.trunc_normal_(self.cls_token, std=0.02)
        self.apply(self._init_module_weights)

    def _init_module_weights(self, m):
        if isinstance(m, nn.Linear):
            nn.init.trunc_normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.LayerNorm):
            nn.init.zeros_(m.bias)
            nn.init.ones_(m.weight)

    def forward(self, x, return_attention=False):
        B = x.shape[0]
        x = self.patch_embed(x)

        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)

        if self.pos_embed is not None:
            x = self.pos_embed(x)
        x = self.pos_drop(x)

        attention_maps = []
        for block in self.blocks:
            x, attn = block(x, return_attention)
            if return_attention:
                attention_maps.append(attn)

        x = self.norm(x)
        cls_output = x[:, 0]
        logits = self.head(cls_output)

        if return_attention:
            return logits, attention_maps
        return logits


# ============================================================================
# 2. DATA LOADING
# ============================================================================

def get_data_loaders(data_dir, batch_size=64, num_workers=4):
    """Create ImageNet-100 data loaders."""
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')

    train_dataset = torchvision.datasets.ImageFolder(train_dir, transform=train_transform)
    val_dataset = torchvision.datasets.ImageFolder(val_dir, transform=val_transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                              num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False,
                            num_workers=num_workers, pin_memory=True)

    return train_loader, val_loader


# ============================================================================
# 3. TRAINING
# ============================================================================

def train_one_epoch(model, loader, optimizer, criterion, device, scaler=None):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    pbar = tqdm(loader, desc='Training')
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()

        if scaler is not None:
            with torch.amp.autocast('cuda'):
                outputs = model(images)
                loss = criterion(outputs, labels)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        pbar.set_postfix({'loss': f'{loss.item():.4f}', 'acc': f'{100.*correct/total:.2f}%'})

    return running_loss / total, 100. * correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in tqdm(loader, desc='Evaluating'):
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)

        running_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    return running_loss / total, 100. * correct / total


def train_model(args):
    """Train a model with specified positional encoding."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    # Set seed
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    train_loader, val_loader = get_data_loaders(args.data_dir, args.batch_size, args.num_workers)

    model = VisionTransformer(
        num_classes=100,
        pe_type=args.pe_type,
        dropout=args.dropout
    ).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    scaler = torch.amp.GradScaler('cuda') if args.amp and torch.cuda.is_available() else None

    output_dir = Path(args.output_dir) / f'{args.pe_type}_seed{args.seed}'
    output_dir.mkdir(parents=True, exist_ok=True)

    best_acc = 0.0
    history = []

    for epoch in range(args.epochs):
        print(f'\nEpoch {epoch+1}/{args.epochs}')
        train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, criterion, device, scaler)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)

        history.append({
            'epoch': epoch + 1,
            'train_loss': train_loss,
            'train_acc': train_acc,
            'val_loss': val_loss,
            'val_acc': val_acc
        })

        print(f'Train Loss: {train_loss:.4f}, Acc: {train_acc:.2f}%')
        print(f'Val Loss: {val_loss:.4f}, Acc: {val_acc:.2f}%')

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save({
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'epoch': epoch,
                'val_acc': val_acc,
                'pe_type': args.pe_type,
                'seed': args.seed,
            }, output_dir / 'best_model.pth')

        with open(output_dir / 'history.json', 'w') as f:
            json.dump(history, f, indent=2)

    print(f'Best validation accuracy: {best_acc:.2f}%')


# ============================================================================
# 4. ATTENTION EXTRACTION
# ============================================================================

def load_model(checkpoint_path, pe_type, device='cuda'):
    """Load trained model from checkpoint."""
    model = VisionTransformer(num_classes=100, pe_type=pe_type).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model


@torch.no_grad()
def extract_attention_maps(model, loader, device, max_samples=None):
    """Extract attention maps from all layers."""
    all_attention = [[] for _ in range(12)]
    all_labels = []
    count = 0

    for images, labels in tqdm(loader, desc='Extracting attention'):
        images = images.to(device)
        _, attention_maps = model(images, return_attention=True)

        for layer_idx, attn in enumerate(attention_maps):
            all_attention[layer_idx].append(attn.cpu())

        all_labels.append(labels)
        count += images.size(0)
        if max_samples and count >= max_samples:
            break

    all_attention = [torch.cat(layer_attn, dim=0)[:max_samples] for layer_attn in all_attention]
    all_labels = torch.cat(all_labels)[:max_samples]

    return all_attention, all_labels


# ============================================================================
# 5. ANALYSIS UTILITIES
# ============================================================================

def entropy_from_attention(attn, eps=1e-12):
    """Compute entropy of attention distributions."""
    p = attn.clamp_min(eps)
    return -(p * p.log()).sum(dim=-1)


def attention_statistics(attention_maps):
    """Compute basic statistics of attention maps."""
    stats = []
    for layer_idx, attn in enumerate(attention_maps):
        ent = entropy_from_attention(attn)
        stats.append({
            'layer': layer_idx + 1,
            'mean_entropy': ent.mean().item(),
            'std_entropy': ent.std().item(),
            'min_entropy': ent.min().item(),
            'max_entropy': ent.max().item()
        })
    return stats


def save_json(obj, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)


# ============================================================================
# 6. CLI
# ============================================================================

def parse_args():
    parser = argparse.ArgumentParser(description='Full-scale ViT positional encoding experiment')
    parser.add_argument('--data_dir', type=str, required=True)
    parser.add_argument('--output_dir', type=str, default='./results')
    parser.add_argument('--mode', type=str, default='train', choices=['train'])
    parser.add_argument('--pe_type', type=str, default='learned', choices=['learned', 'sinusoidal', 'rope', 'alibi'])
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--num_workers', type=int, default=4)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--lr', type=float, default=3e-4)
    parser.add_argument('--weight_decay', type=float, default=0.05)
    parser.add_argument('--dropout', type=float, default=0.0)
    parser.add_argument('--amp', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    train_model(args)


if __name__ == '__main__':
    main()
