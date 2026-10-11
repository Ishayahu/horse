import json,pathlib,urllib.request,re,unicodedata,hashlib,concurrent.futures
R=pathlib.Path(__file__).parent; C=pathlib.Path('/tmp/horse-kab-cache')
C.mkdir(parents=True,exist_ok=True)
I=R/'KAB-001.inventory.json'
# Replay the persisted whitelist by default, preserving the bounded original scope.
raw=I.read_bytes(); prior=json.loads(raw); selected=prior['selected']
Q=['סוס','סוסיא','סוסין','סוס ורכבו','סוס ורוכבו','לסוסתי','לא ירבה']
def clean(s):return ''.join(c for c in re.sub('<[^>]*>','',s) if not unicodedata.combining(c))
def leaves(x,p=()):
 if isinstance(x,str):yield p,x
 elif isinstance(x,list):
  for i,v in enumerate(x,1):yield from leaves(v,p+(i,))
 elif isinstance(x,dict):
  for k,v in x.items():yield from leaves(v,p+(k,))
def fetch(b):
 raw=urllib.request.urlopen(b['json_url'],timeout=45).read(); d=json.loads(raw)
 (C/(b['title'].replace(' ','_')+'.json')).write_bytes(raw)
 hits=[];ss=list(leaves(d.get('text',{})))
 for path,s in ss:
  c=clean(s); qs=[q for q in Q if q in c]
  if qs:hits.append(dict(work=b['title'],path=list(path),queries=qs,excerpt=c[:120],status='candidate_not_verified'))
 return dict(work=b['title'],url=b['json_url'],sha256=hashlib.sha256(raw).hexdigest(),versions=d.get('versions'),leaf_count=len(ss),candidate_count=len(hits),text_structure=list(d.get('text',{})) if isinstance(d.get('text'),dict) else 'list'),hits
manifest=[];hits=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for b,f in [(b,ex.submit(fetch,b)) for b in selected]:
  try:m,h=f.result();manifest.append(m);hits+=h;print(b['title'],m['leaf_count'],len(h))
  except Exception as e:manifest.append(dict(work=b['title'],error=str(e)));print('ERROR',b['title'],e)
(R/'KAB-001.inventory.json').write_text(json.dumps(dict(schema_version=1,task_id='KAB-001',inventory_url='https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/books.json',inventory_cache_reused=None,inventory_sha256=prior['inventory_sha256'],whitelist_replayed_from=str(I),selected=selected,searched=manifest,queries=Q,normalization='strip HTML and Unicode combining marks; substring matching; false positives retained'),ensure_ascii=False,indent=2))
(R/'KAB-001.candidates.jsonl').write_text(''.join(json.dumps(h,ensure_ascii=False)+'\n' for h in hits))
