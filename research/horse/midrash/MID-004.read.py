import json,urllib.request,concurrent.futures,pathlib
from urllib.parse import quote
R=pathlib.Path(__file__).parent
refs=['Bereshit Rabbah.52.7','Bereshit Rabbah.68.9','Bereshit Rabbah.68.10','Bereshit Rabbah.75.10','Pirkei DeRabbi Eliezer.42.6','Midrash Tehillim.18.12','Midrash Tehillim.21.2','Midrash Tanchuma, Bereshit.7.11','Pesikta Rabbati.12']
def get(ref):
 u='https://www.sefaria.org/api/texts/'+quote(ref)+'?lang=he&context=1';d=json.load(urllib.request.urlopen(u,timeout=35))
 return dict(request=ref,url=u,ref=d.get('ref'),sectionRef=d.get('sectionRef'),sections=d.get('sections'),sectionNames=d.get('sectionNames'),heVersionTitle=d.get('heVersionTitle'),heVersionSource=d.get('heVersionSource'),he=d.get('he'),heLicense=d.get('heLicense'),error=d.get('error'))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 rs=list(ex.map(get,refs))
# Temporary full context; committed report will only contain selected quotes and metadata.
pathlib.Path('/tmp/MID-004.context.json').write_text(json.dumps(rs,ensure_ascii=False))
for r in rs:
 print(r['request'],r['ref'],r['sectionNames'],r['sections'],r['heVersionTitle'])
 text=r['he'];i=(r['sections'] or [1])[-1]-1
 if isinstance(text,list):print(text[i] if i<len(text) else text[:1])
 else:print(str(text)[:1000])
