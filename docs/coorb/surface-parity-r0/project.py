#!/usr/bin/env python3
"""Pure offline multi-surface projections for one source-bound work object."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

REQUIRED = ('schema','object_id','class','title','why','currentness','source','evidence','authority','privacy','receiver','next','challenge','recover','lanes','unknowns','nonclaims')
INVARIANTS = ('object_id','class','currentness','source','evidence','authority','privacy','receiver')
VIEWS = ('glance','orb','map','machine')

def canonical(o):
    return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'))

def validate(o):
    if not isinstance(o,dict) or any(k not in o for k in REQUIRED): raise ValueError('missing required object fields')
    if o['schema'] != 'CoCivium.CoOrbSurfaceParity.R0': raise ValueError('unsupported schema')
    if not isinstance(o['object_id'],str) or not o['object_id'].strip(): raise ValueError('missing identity')
    if o['authority']['effects_authorized'] is not False: raise ValueError('no effect authority permitted')
    if o['privacy']['class']!='PUBLIC_SYNTHETIC' or o['privacy']['personal_content_included'] is not False: raise ValueError('private data forbidden')
    if o['receiver']['independent_ack'] is not False: raise ValueError('no fake receiver ACK')
    if o['currentness']['state'] != 'UNVERIFIED_LIVE': raise ValueError('live status is not proven')
    if o['evidence']['claim_verified'] is not False: raise ValueError('fictional demo is not evidence')
    if not isinstance(o['lanes'],list) or not 1<=len(o['lanes'])<=12: raise ValueError('lane count out of bounds')
    if any(not isinstance(l,dict) or any(k not in l for k in ('id','label','status','concern')) for l in o['lanes']): raise ValueError('invalid lane')
    return o

def project(source,view):
    validate(source)
    if view not in VIEWS: raise ValueError('invalid view')
    src=copy.deepcopy(source)
    common={k:src[k] for k in INVARIANTS}
    if view=='glance': visible={'title':src['title'],'why':src['why'],'next':src['next']}
    elif view=='orb': visible={'title':src['title'],'why':src['why'],'next':src['next'],'challenge':src['challenge'],'recover':src['recover'],'unknowns':src['unknowns']}
    elif view=='map': visible={'title':src['title'],'lanes':src['lanes'],'unknowns':src['unknowns'],'next':src['next']}
    else: visible={k:v for k,v in src.items() if k not in INVARIANTS}
    loss=sorted(set(src)-set(INVARIANTS)-set(visible))
    return {'projection_schema':'CoCivium.CoOrbSurfaceParity.View.R0','view':view,
            'source_sha256':hashlib.sha256(canonical(src).encode()).hexdigest(),
            'shared_invariants':common,'visible':visible,'projection_omissions':loss,
            'effects':{'network':0,'provider_calls':0,'workers_spawned':0,'source_mutations':0}}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,default=Path(__file__).with_name('work-object.json'))
    p.add_argument('--view',choices=VIEWS,default='glance')
    args=p.parse_args()
    obj=json.loads(args.source.read_text(encoding='utf-8'))
    print(json.dumps(project(obj,args.view),sort_keys=True,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
