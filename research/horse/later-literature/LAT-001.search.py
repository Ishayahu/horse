import json,pathlib,urllib.request,concurrent.futures,re,unicodedata,hashlib
R=pathlib.Path(__file__).parent
index=R/'LAT-001.inventory-cache.json'
if not index.exists():
 index.write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/books.json',timeout=50).read())
allb=json.loads(index.read_text())['books']
titles=['Gevurot Hashem',"Be'er HaGolah",'Guide for the Perplexed','Devash LeFi','Midbar Kedemot','Chomat Anakh on II Kings','Chomat Anakh on Zechariah','Petach Einayim on Berakhot','Petach Einayim on Pesachim','Petach Einayim on Sanhedrin']
selected=[b for b in allb if b['title'] in titles and b.get('language')=='Hebrew' and b.get('versionTitle')=='merged']
def clean(s):return ''.join(c for c in re.sub('<[^>]*>','',s) if not unicodedata.combining(c))
def leaves(x,p=()):
 if isinstance(x,str):yield p,x
 elif isinstance(x,list):
  for i,v in enumerate(x,1):yield from leaves(v,p+(i,))
 elif isinstance(x,dict):
  for k,v in x.items():yield from leaves(v,p+(k,))
def fetch(b):
 raw=urllib.request.urlopen(b['json_url'],timeout=50).read();d=json.loads(raw)
 (R/('LAT-001.cache.'+re.sub('[^a-zA-Z0-9]','_',b['title'])+'.json')).write_bytes(raw)
 hits=[];ss=list(leaves(d.get('text',{})))
 for p,s in ss:
  c=clean(s)
  qs=[q for q in ['סוס','רכב אש','רוכב','מרכבה','לא ירבה','רכב ישראל'] if q in c]
  if qs:hits.append(dict(work=b['title'],path=list(p),queries=qs,text=c,source_url=b['json_url'],status='discovery_not_interpreted'))
 return dict(work=b['title'],url=b['json_url'],sha256=hashlib.sha256(raw).hexdigest(),versions=d.get('versions'),leaf_count=len(ss),top_keys=list(d),candidate_count=len(hits)),hits
manifest=[];hits=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 fs={ex.submit(fetch,b):b for b in selected}
 for f in concurrent.futures.as_completed(fs):
  b=fs[f]
  try:m,h=f.result();manifest.append(m);hits+=h;print(b['title'],m['leaf_count'],len(h))
  except Exception as e:manifest.append(dict(work=b['title'],url=b['json_url'],error=str(e)));print('ERROR',b['title'],e)
(R/'LAT-001.manifest.json').write_text(json.dumps(dict(schema_version=1,task_id='LAT-001',inventory_url='https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/books.json',selected=selected,searched=manifest,queries=['סוס','רכב אש','רוכב','מרכבה','לא ירבה','רכב ישראל']),ensure_ascii=False,indent=2))
(R/'LAT-001.candidates.jsonl').write_text(''.join(json.dumps(h,ensure_ascii=False)+'\n' for h in hits))
