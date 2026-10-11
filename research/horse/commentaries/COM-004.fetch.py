import json,pathlib,urllib.request,urllib.parse,concurrent.futures,html,re,collections
p=pathlib.Path(__file__).resolve().parent;cache=pathlib.Path('/tmp/horse-com004-cache');cache.mkdir(exist_ok=True)
authors=['Abarbanel','Sforno','Ibn Ezra'];targets={'II Kings':['2:11','6:17'],'Zechariah':['1:8']+['6:'+str(i) for i in range(1,9)]}
def get(u):
 try:
  with urllib.request.urlopen(u,timeout=45) as f:return json.load(f)
 except Exception as e:return {'fetch_error':str(e)}
def f(x):
 a,b=x;t=a+' on '+b;k=t.replace(' ','_');reuse=pathlib.Path('/tmp/horse-com003-cache')/(k+'.json');cp=cache/(k+'.json');iu='https://www.sefaria.org/api/index/'+urllib.parse.quote(k);tu='https://www.sefaria.org/api/texts/'+urllib.parse.quote(k)+'?context=0&pad=0'
 if reuse.exists():e=json.load(open(reuse))
 elif cp.exists():e=json.load(open(cp))
 else:
  ix=get(iu);d={} if ix.get('error') else get(tu);e=dict(author=a,book=b,title=t,index_url=iu,text_url=tu,index=ix,data=d);cp.write_text(json.dumps(e,ensure_ascii=False))
 return e
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:exports=list(ex.map(f,[(a,b) for b in targets for a in authors]))
cells=[];raw=[]
for e in exports:
 ix=e['index'];d=e['data'];h=d.get('he');
 for v in targets[e['book']]:
  c,n=map(int,v.split(':'));ts=None
  if isinstance(h,list):
   try:ts=h[c-1][n-1]
   except(IndexError,TypeError):ts=[]
  status='present' if ts else 'empty' if ts is not None else 'missing' if ix.get('error') or d.get('error') else 'unavailable'
  z=dict(author=e['author'],book=e['book'],verse=v,title=e['title'],status=status,scanned=ts is not None,index_url=e['index_url'],api_url=e['text_url'],index_title=ix.get('title'),error=ix.get('error') or ix.get('fetch_error') or d.get('fetch_error'),segment_count=len(ts or []));cells.append(z)
  if ts:raw.append(dict(**z,segments=[html.unescape(re.sub('<[^>]+>','',s)) for s in ts]))
(p/'COM-004.coverage.json').write_text(json.dumps(dict(schema_version=1,task_id='COM-004',cells=cells,counts=dict(collections.Counter(c['status'] for c in cells)),limitations=['Unavailable indexed title is not absence in all traditional editions.','Empty exact verse may have grouped discussion elsewhere.']),ensure_ascii=False,indent=2));(p/'COM-004.discoveries.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in raw))
(p/'COM-004.manifest.json').write_text(json.dumps([dict(author=e['author'],book=e['book'],index_url=e['index_url'],index=e['index'],text_url=e['text_url'],returned_ref=e['data'].get('ref'),available_hebrew_versions=[v for v in e['data'].get('versions',[]) if v.get('language')=='he']) for e in exports],ensure_ascii=False,indent=2));print(collections.Counter(c['status'] for c in cells))
