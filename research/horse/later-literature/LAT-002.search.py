import json,pathlib,urllib.request,concurrent.futures,re,unicodedata,hashlib
R=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/horse-lat002-cache');C.mkdir(exist_ok=True)
IU='https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/books.json'
raw=urllib.request.urlopen(IU,timeout=45).read();books=json.loads(raw)['books']
whitelist=['Nachal Kedumim on Torah','Penei David','Mesillat Yesharim','Derekh Hashem',"Da'at Tevunot",'Kalach Pitchei Chokhmah','Asarah Perakim LeRamchal','Derech Etz Chayim (Ramchal)','Tanya','Kedushat Levi','Degel Machaneh Ephraim','Aderet Eliyahu','Beur HaGra on Sifra DeTzniuta']
sel=[b for b in books if b.get('language')=='Hebrew' and b.get('versionTitle')=='merged' and (b['title'] in whitelist or b['title'].startswith('Chomat Anakh on'))]
prior={'Chomat Anakh on II Kings','Chomat Anakh on Zechariah'}
def clean(s):return ''.join(c for c in re.sub('<[^>]*>','',s) if not unicodedata.combining(c))
def leaves(x,p=()):
 if isinstance(x,str):yield p,x
 elif isinstance(x,list):
  for i,v in enumerate(x,1):yield from leaves(v,p+(i,))
 elif isinstance(x,dict):
  for k,v in x.items():yield from leaves(v,p+(k,))
pat=re.compile(r'(?<![א-ת])(?:[ובכלמשה]{0,3})סוס(?:ים|י|יך|יו|יא|ין|ן|\')?(?![א-ת])')
Q=['סוס','סוס ורכבו','סוס ורוכבו','לסוסתי','לא ירבה','רכב אש','סוסי אש','רכב ישראל','כסוס כפרד']
def fetch(b):
 raw=urllib.request.urlopen(b['json_url'],timeout=45).read();d=json.loads(raw);(C/(re.sub('[^a-zA-Z0-9]','_',b['title'])+'.json')).write_bytes(raw)
 hits=[];ss=list(leaves(d.get('text',{})))
 for p,s in ss:
  c=clean(s);qs=[q for q in Q if q in c]
  if qs:
   pos=min(c.find(q) for q in qs);hits.append(dict(work=b['title'],path=list(p),queries=qs,equine_token_candidate=bool(pat.search(c)),excerpt=c[max(0,pos-90):pos+550],text_sha256=hashlib.sha256(c.encode()).hexdigest(),source_url=b['json_url'],status='discovery_not_interpreted'))
 versions=[v for v in books if v['title']==b['title'] and v.get('language')=='Hebrew' and v.get('versionTitle')!='merged']
 licenses=[]
 for v in versions:
  try:
   # Version metadata fetched from the version export; never guess merged licensing.
   vv=json.load(urllib.request.urlopen(v['json_url'],timeout=30));licenses.append(dict(versionTitle=v['versionTitle'],url=v['json_url'],license=vv.get('license'),versionSource=vv.get('versionSource'),status='fetched_metadata'))
  except Exception as e:licenses.append(dict(versionTitle=v['versionTitle'],url=v['json_url'],error=str(e)))
 return dict(work=b['title'],url=b['json_url'],sha256=hashlib.sha256(raw).hexdigest(),versions=d.get('versions'),leaf_count=len(ss),candidate_count=len(hits),equine_token_candidate_count=sum(h['equine_token_candidate'] for h in hits),named_version_metadata=licenses,range='All supplied text leaves; close reading only selected passages',status='lexically_searched'),hits
manifest=[];hits=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 fs={ex.submit(fetch,b):b for b in sel if b['title'] not in prior}
 for f in concurrent.futures.as_completed(fs):
  b=fs[f]
  try:m,h=f.result();manifest.append(m);hits+=h;print(b['title'],m['leaf_count'],len(h),flush=True)
  except Exception as e:manifest.append(dict(work=b['title'],url=b['json_url'],status='access_failed',error=str(e)));print('ERROR',b['title'],e,flush=True)
for b in sel:
 if b['title'] in prior:manifest.append(dict(work=b['title'],status='prior_batch_searched_not_repeated',prior_result='LAT-001.manifest.json',url=b['json_url']))
(R/'LAT-002.manifest.json').write_text(json.dumps(dict(schema_version=1,task_id='LAT-002',inventory_url=IU,inventory_sha256=hashlib.sha256(raw).hexdigest(),whitelist=whitelist,collection='All 35 catalogued Chomat Anakh on biblical-book exports; two reused from LAT001',selected=sel,searched=manifest,queries=Q,normalization='HTML stripped, combining marks removed, substring candidates then Hebrew token filter; no completeness inference beyond exact digital ranges'),ensure_ascii=False,indent=2))
(R/'LAT-002.candidates.jsonl').write_text(''.join(json.dumps(h,ensure_ascii=False)+'\n' for h in hits))
