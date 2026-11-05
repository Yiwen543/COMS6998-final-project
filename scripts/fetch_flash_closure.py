"""Reproduce the exact public Flash dependency snapshot without API credentials."""
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path
from run_midterm_fixed import ROOT


def fetch(manifest,output):
    m=json.loads(manifest.read_text())
    for f in m['files']:
        path=Path(f['path'])
        if path.is_absolute() or '..' in path.parts:raise ValueError('Invalid manifest path')
        p=output/path
        if p.exists():b=p.read_bytes()
        else:
            url='https://raw.githubusercontent.com/lowRISC/opentitan/'+m['revision']+'/'+f['path']
            with urllib.request.urlopen(url,timeout=60) as r:b=r.read()
        blob=hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()
        if blob!=f['blob'] or hashlib.sha256(b).hexdigest()!=f['sha256']:
            raise ValueError('Pinned content mismatch; refusing to overwrite: '+f['path'])
        if not p.exists():p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        print(f['path']+' verified')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--manifest',type=Path,default=ROOT/'results/natural_ip_integration_20261104/flash-sources.json')
    p.add_argument('--output',type=Path,default=ROOT/'third_party/opentitan_flash_closure')
    a=p.parse_args();fetch(a.manifest,a.output)
