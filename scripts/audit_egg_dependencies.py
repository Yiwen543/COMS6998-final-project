#!/usr/bin/env python3
"""Re-solve archived typed prerequisites, replay prior-only proof paths and audit accounting without native search."""
import argparse
from pathlib import Path

from egg_dependency_workload import ARCHIVE,LIVE_ARCHIVE
from run_egg_dependencies import run

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,default=ARCHIVE);parser.add_argument('--live-archive',type=Path,default=LIVE_ARCHIVE)
    parser.add_argument('--run-dir',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--triage',action='store_true',help='audit the separate typed-triage ablation')
    args=parser.parse_args();result=run(args.archive,args.live_archive,None,args.output,replay_dir=args.run_dir,triage=args.triage)
    print(f"Independently audited {result['requests']} comparisons, {result['groups']} groups, {len(result['arms'])} arms; zero native re-search.")
