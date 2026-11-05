"""Reuse the bounded isolated author/reviewer transport without changing history."""
import argparse
import json
from pathlib import Path
import run_i2c_checker_roles as transport
from run_midterm_fixed import sha

def run(packet,output,prior=None):
    manifest=json.loads((packet/'manifest.json').read_text())
    for name in ('packet','prompt'):
        f=packet/('packet.json' if name=='packet' else 'prompt.txt')
        if sha(f)!=manifest[name+'_sha256']:raise ValueError('Prepared packet drift')
    original=transport.call
    def call(prompt,path,env,role):return original(prompt,path,env,role.replace('I2C','SPI core'))
    transport.call=call
    try:transport.run(packet,output,prior)
    finally:
        transport.call=original
        if output.exists():
            (output/'role-wrapper.json').write_text(json.dumps({'scope':'original spi_host_core','wrapper_sha256':sha(Path(__file__)),'transport_sha256':sha(Path(transport.__file__)),'role':'Separate Claude author and fresh read-only reviewer; GPT owns driver/stimulus only.'},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--prior',type=Path)
    a=p.parse_args();run(a.packet.resolve(),a.output.resolve(),a.prior.resolve() if a.prior else None)
