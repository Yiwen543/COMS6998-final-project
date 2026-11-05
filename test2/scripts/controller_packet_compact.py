#!/usr/bin/env python3
"""Lossless shared coverage dictionary codec, no source/evidence selection."""
import copy
import json
from common import BASE,dump,sha

TASK=BASE/'tasks/axis_length_fifo_v1'


def pack(raw):
    strings=[];vectors=[]
    def string(v):
        if v is None:return None
        if v not in strings:strings.append(v)
        return strings.index(v)
    def vector(v):
        if v not in vectors:vectors.append(v)
        return vectors.index(v)
    ordinary=[]
    for row in raw['ordinary_rows']:
        row=copy.deepcopy(row)
        for i in (0,3,4,5,6):row[i]=string(row[i])
        ordinary.append(row[:7]+[vector(row[7:])])
    toggle=[]
    for entry in raw['toggle_sites']:
        site=copy.deepcopy(entry['site'])
        for i in (0,3,4):site[i]=string(site[i])
        bits=entry['bits']
        contiguous=bool(bits) and bits==list(range(bits[0],bits[0]+len(bits)))
        bit_repr=['range',bits[0],len(bits)] if contiguous else ['list',bits]
        toggle.append([site,bit_repr,[vector(v) for v in entry['hits_rle']]])
    return dict(encoding='coverage_dictionary_v1',strings=strings,vectors=vectors,ordinary=ordinary,toggle=toggle,
                metadata={k:v for k,v in raw.items() if k not in ('ordinary_rows','toggle_sites')},
                decode='ordinary:8 columns; columns0/3/4/5/6 index strings (null stays null), column7 indexes vector of three trace hits. toggle:[site,bits,three vector IDs]; site0/3/4 index strings. bits range=[range,start,count] or list=[list,values]; vectors restore original RLE arrays. Metadata restores all other fields. Every source counter and per-trace count stays separate.')


def unpack(data):
    if data['encoding']!='coverage_dictionary_v1':raise ValueError('Unknown codec')
    strings=data['strings'];vectors=data['vectors'];raw=copy.deepcopy(data['metadata'])
    raw['ordinary_rows']=[]
    for encoded in data['ordinary']:
        row=copy.deepcopy(encoded[:7])
        for i in (0,3,4,5,6):row[i]=strings[row[i]] if row[i] is not None else None
        raw['ordinary_rows'].append(row+copy.deepcopy(vectors[encoded[7]]))
    raw['toggle_sites']=[]
    for encoded in data['toggle']:
        site,bit_repr,ids=copy.deepcopy(encoded)
        for i in (0,3,4):site[i]=strings[site[i]] if site[i] is not None else None
        bits=list(range(bit_repr[1],bit_repr[1]+bit_repr[2])) if bit_repr[0]=='range' else bit_repr[1]
        raw['toggle_sites'].append(dict(site=site,bits=bits,hits_rle=[copy.deepcopy(vectors[i]) for i in ids]))
    return raw


def execute():
    origin=TASK/'qualification/prompt-audit-v2';out=TASK/'qualification/prompt-audit-v3';out.mkdir(exist_ok=False)
    packets={};audit={}
    for arm in ('B2_raw','C2_semantic'):
        path=origin/(arm+'.json');old=json.loads(path.read_text());new=copy.deepcopy(old)
        new['raw_coverage']=pack(old['raw_coverage'])
        restored=copy.deepcopy(new);restored['raw_coverage']=unpack(new['raw_coverage'])
        assert restored==old
        target=out/(arm+'.json');dump(target,new)
        packets[arm]=new
        audit[arm]=dict(source_packet_sha256=sha(path),packet_sha256=sha(target),compact_json_bytes=len(json.dumps(new,separators=(',',':'),sort_keys=True).encode()),full_packet_roundtrip=True)
    c=copy.deepcopy(packets['C2_semantic']);c.pop('egraph_feedback');assert c==packets['B2_raw']
    dump(out/'summary.json',dict(status='passed',policy='Exact common information re-encoding before any candidate calls; caps unchanged; failed provider counts retained. Complete RTL/spec/observations/semantic groups unchanged.',counter_count=3168,shared_packet_equal_except_egraph=True,arms=audit,codec_sha256=sha(__file__)))
    print(json.dumps(audit,indent=2))


if __name__=='__main__':execute()
