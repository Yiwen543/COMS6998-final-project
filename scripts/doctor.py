#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
versions = {}
for name, flag in [('python3','--version'),('verilator','--version'),('iverilog','-V'),('vvp','-V'),('yosys','-V'),('cargo','--version'),('rustc','--version'),('c++','--version')]:
    path = shutil.which(name)
    if not path:
        print(f'MISSING {name}; see README.md', file=sys.stderr)
        sys.exit(1)
    proc = subprocess.run([path,flag],text=True,capture_output=True,check=True)
    versions[name] = {'path':path, 'version':(proc.stdout or proc.stderr).splitlines()[0]}
help_text=subprocess.run(['verilator','--help'],text=True,capture_output=True,check=True).stdout
if '--coverage-expr' not in help_text: sys.exit('Verilator with --coverage-expr is required; tested with 5.050')
print(json.dumps(versions,indent=2))
