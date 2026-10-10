import json,pathlib,urllib.request,urllib.parse,concurrent.futures,collections,re,html
out=pathlib.Path('horse-check/research/commentaries');cache=pathlib.Path('/tmp/horse-com003-cache');cache.mkdir(exist_ok=True)
books=dict(zip('Gen Exod Deut Josh Judg 2Sam 1Kgs 2Kgs Isa Jer Ezek Hos Joel Amos Mic Nah Hab Hag Zech Ps Job Prov Eccl Song Ezra Neh Esth 2Chr'.split(),['Genesis','Exodus','Deuteronomy','Joshua','Judges','II Samuel','I Kings','II Kings','Isaiah','Jeremiah','Ezekiel','Hosea','Joel','Amos','Micah','Nahum','Habakkuk','Haggai','Zechariah','Psalms','Job','Proverbs','Ecclesiastes','Song of Songs','Ezra','Nehemiah','Esther','II Chronicles']))
authors=['Rashi','Ibn Ezra','Metzudat David','Metzudat Zion']
base=[json.loads(l) for l in open('horse-check/research/tanakh/TAN-001.direct.jsonl')]
reuse={(r['author'],r['book'],r['verse']):r for r in json.loads((out/'COM-002.raw.json').read_text())}
def get(url):
 try:
  with urllib.request.urlopen(url,timeout=50) as f:return json.load(f)
 except Exception as e:return {'fetch_error':str(e)}
def fetch(pair):
 a,b=pair;title=a+' on '+b;key=title.replace(' ','_');p=cache/(key+'.json');iu='https://www.sefaria.org/api/index/'+urllib.parse.quote(key);tu='https://www.sefaria.org/api/texts/'+urllib.parse.quote(key)+'?context=0&pad=0'
 if p.exists():return json.loads(p.read_text())
 ix=get(iu);d=get(tu) if not ix.get('error') and not ix.get('fetch_error') else {};r=dict(author=a,book=b,title=title,index_url=iu,text_url=tu,index=ix,data=d);p.write_text(json.dumps(r,ensure_ascii=False));return r
pairs=[(a,b) for b in books.values() for a in authors]
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:exports=list(ex.map(fetch,pairs))
lookup={(r['author'],r['book']):r for r in exports};cells=[];raw=[]
for r in base:
 _,c,v=r['locator'].split('.');b=books[r['work']]
 for a in authors:
  rr=reuse.get((a,b,c+':'+v));e=lookup[a,b];ix=e['index'];d=e['data'];texts=None;mode='per-book export'
  if rr: d=rr['data'];texts=d.get('he');url=rr['api_url'];mode='COM-002 reused verse response'
  else:
   url=e['text_url'];h=d.get('he')
   if isinstance(h,list):
    try:texts=h[int(c)-1][int(v)-1]
    except (IndexError,TypeError):texts=[]
  status='present' if texts else 'empty' if texts is not None else 'missing' if ix.get('error') or d.get('error') else 'unavailable'
  if texts is not None and not isinstance(texts,list):texts=[texts]
  cell=dict(author=a,book=b,verse=c+':'+v,parent_source_id=r['id'],status=status,retrieval=mode,title=e['title'],index_url=e['index_url'],api_url=url,index_title=ix.get('title'),base_text_titles=ix.get('base_text_titles'),he_version_title=d.get('heVersionTitle'),error=ix.get('error') or ix.get('fetch_error') or d.get('error') or d.get('fetch_error'),segment_count=len(texts or []))
  cells.append(cell)
  if texts:raw.append(dict(**cell,segments=[html.unescape(re.sub('<[^>]+>','',t)) for t in texts if isinstance(t,str)]))
(out/'COM-003.coverage.json').write_text(json.dumps(dict(schema_version=1,task_id='COM-003',base_verses=129,authors=authors,cells=cells,counts=dict(collections.Counter(c['status'] for c in cells)),limits=['Status missing means requested indexed title not accessible, not absence in the tradition.','Present is retrieval coverage only.','Empty may reflect comments grouped at neighbouring verses.']),ensure_ascii=False,indent=2))
(out/'COM-003.discoveries.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in raw))
print(collections.Counter(c['status'] for c in cells));print('exports',len(exports),'raw cells',len(raw))
