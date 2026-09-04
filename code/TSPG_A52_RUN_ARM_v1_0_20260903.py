#!/usr/bin/env python3
from pathlib import Path
import argparse,sys
HERE=Path(__file__).resolve().parent.parent; sys.path.insert(0,str(HERE/'code'))
from TSPG_A52_RUNTIME_CORE_v1_0_20260903 import run_arm
ap=argparse.ArgumentParser(); ap.add_argument('--arm',choices=['PV-A','PV-B1','PV-B2','PV-C'],required=True); ap.add_argument('--output-root',required=True); ap.add_argument('--device',default='cuda'); a=ap.parse_args(); out=Path(a.output_root)/a.arm; run_arm(HERE,a.arm,out,a.device)
