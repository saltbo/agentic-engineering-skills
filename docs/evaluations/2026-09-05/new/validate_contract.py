"""Offline targeted contract checks. Not a general OpenAPI meta-schema validator."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

doc=json.loads(Path('openapi.json').read_text())
checks=0

def check(condition, message):
    global checks
    assert condition, message
    checks += 1

def resolve(value):
    if '$ref' not in value: return value
    pointer=value['$ref']
    check(pointer.startswith('#/'),f'Nonlocal reference: {pointer}')
    result=doc
    for part in pointer[2:].split('/'):
        result=result[part.replace('~1','/').replace('~0','~')]
    return {**result,**{k:v for k,v in value.items() if k!='$ref'}}

def walk(value):
    if isinstance(value,dict):
        if '$ref' in value: resolve(value)
        for child in value.values(): walk(child)
    elif isinstance(value,list):
        for child in value: walk(child)
walk(doc)

def valid(value,s):
    s=resolve(s)
    kind=s.get('type')
    if kind=='object':
        assert isinstance(value,dict)
        assert set(s.get('required',[])) <= value.keys()
        props=s.get('properties',{})
        if s.get('additionalProperties') is False: assert value.keys() <= props.keys()
        for k,v in value.items():
            if k in props: valid(v,props[k])
    elif kind=='array':
        assert isinstance(value,list)
        assert len(value)>=s.get('minItems',0)
        assert len(value)<=s.get('maxItems',float('inf'))
        for v in value: valid(v,s['items'])
    elif kind=='integer':
        assert isinstance(value,int) and not isinstance(value,bool)
        assert s.get('minimum',-float('inf'))<=value<=s.get('maximum',float('inf'))
    elif kind=='string':
        assert isinstance(value,str)
        assert s.get('minLength',0)<=len(value)<=s.get('maxLength',float('inf'))
        if 'pattern' in s: assert re.search(s['pattern'],value)
        if s.get('format')=='uri': assert urlparse(value).scheme
    else: raise AssertionError(f'Unexpected schema kind: {kind}')
    if 'enum' in s: assert value in s['enum']

def reject(value,s):
    try: valid(value,s)
    except AssertionError: return
    raise AssertionError(f'Accepted invalid input: {value}')
check(doc['openapi']=='3.1.0','OpenAPI dialect')
check(set(doc['paths'])=={'/orders','/orders/{orderId}'},'Canonical paths')
ids=[]
for path,item in doc['paths'].items():
    for method,op in item.items():
        check(method in ['get','post'],'Requested operation only')
        ids.append(op['operationId'])
        check(op['security']==[{'bearerAuth':[]}],'Explicit authentication')
        check(op['tags']==['Orders'],'One primary domain tag')
        for p in op['parameters']:
            p=resolve(p)
            check(all(k in p for k in ['name','in','required','style','schema']),'Parameter definition')
            if p['in']=='path': check(p['required'] and '{'+p['name']+'}' in path,'Path binding')
            if 'default' in resolve(p['schema']): valid(resolve(p['schema'])['default'],p['schema'])
        for code,r in op['responses'].items():
            r=resolve(r)
            check('Request-Id' in r['headers'],'Response correlation')
            for media,body in r['content'].items():
                valid(body['example'],body['schema'])
                if int(code)>=400:
                    check(media=='application/problem+json','Problem media')
                    check(body['example']['status']==int(code),'Problem status')
        if 'requestBody' in op:
            for body in op['requestBody']['content'].values(): valid(body['example'],body['schema'])
check(set(ids)=={'createOrder','getOrder','listOrders'} and len(ids)==3,'Unique operation IDs')
for s in doc['components']['schemas'].values():
    if 'example' in s: valid(s['example'],s)
for h in doc['components']['headers'].values():
    if 'example' in h: valid(h['example'],h['schema'])
create=doc['components']['schemas']['CreateOrder']
for bad in [{},{'totalCents':-1},{'totalCents':1.5},{'totalCents':True},{'totalCents':None},{'totalCents':0,'status':'shipped'},{'totalCents':0,'tenantId':'other'},{'totalCents':0,'id':'supplied'},{'totalCents':9007199254740992}]: reject(bad,create)
for amount in [0,1299,9007199254740991]: valid({'totalCents':amount},create)
reject('cancelled',doc['components']['schemas']['OrderStatus'])
for name,values in [('Page',[0,-1,1.5]),('PageSize',[0,101]),('IdempotencyKey',['unquoted','""'])]:
    for value in values: reject(value,doc['components']['parameters'][name]['schema'])
for total,page,size in [(0,1,50),(1,1,50),(101,2,50),(101,4,50)]:
    pages=(total+size-1)//size
    count=max(0,min(size,total-(page-1)*size))
    payload={'items':[doc['components']['schemas']['Order']['example']]*count,'pagination':{'page':page,'pageSize':size,'totalItems':total,'totalPages':pages}}
    valid(payload,doc['components']['schemas']['OrderCollection'])
check('links' not in doc['components']['schemas']['OrderCollection']['properties'],'No body navigation links')
print(f'PASS: {checks} structural assertions; reference resolution, examples, negative input cases and page edge cases passed.')
print('LIMITATION: targeted offline checks only; a full OpenAPI meta-schema validator and server runtime are unavailable.')
