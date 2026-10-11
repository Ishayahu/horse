import urllib.request,json,concurrent.futures,pathlib,time
out=pathlib.Path('horse-check/research/commentaries');out.mkdir(exist_ok=True,parents=True)
targets={'Job':['39:'+str(v) for v in range(19,26)],'Song of Songs':['1:9'],'Psalms':['20:8','33:17','147:10'],'Isaiah':['31:'+str(v) for v in range(1,4)],'Deuteronomy':['20:1'],'Exodus':['15:1']}
authors=['Rashi','Ibn Ezra','Radak','Metzudat David','Malbim','Or HaChaim','Kli Yakar']
def get(p):
 try:
  with urllib.request.urlopen('https://www.sefaria.org/api/'+p,timeout=35) as r:return json.load(r)
 except Exception as e:return {'fetch_error':str(e)}
def task(x):
 a,b,v=x;ref=a+' on '+b+' '+v;u='texts/'+urllib.parse.quote(ref.replace(' ','_'))+'?context=0&pad=0';d=get(u)
 return {'author':a,'book':b,'verse':v,'ref':ref,'api_url':'https://www.sefaria.org/api/'+u,'data':d}
xs=[(a,b,v) for b,vs in targets.items() for a in authors for v in vs]
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
 rows=list(ex.map(task,xs))
(out/'COM-002.raw.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for x in rows:
 d=x['data'];he=d.get('he');status='present' if he else ('missing' if d.get('error') else 'empty' if 'he' in d else 'unavailable')
 print(x['ref'],status,str(he)[:120])
