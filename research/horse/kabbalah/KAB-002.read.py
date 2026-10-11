import json,pathlib,urllib.request,concurrent.futures
from urllib.parse import quote
R=pathlib.Path(__file__).parent
refs=['Sefer Etz Chaim.49.7.2','Pri Etz Chaim, Gate of Songs.6.8',"Sha'ar Ma'amarei Rashbi, Parashat Kedoshim.1","Sha'ar Ma'amarei Rashbi, Parashat Kedoshim.2","Sha'ar HaPesukim, Book of Psalms.58","Sha'ar HaPesukim, Book of Psalms.59","Sha'ar Ruach HaKodesh.129.20"]
def fetch(ref):
 u='https://www.sefaria.org/api/texts/'+quote(ref)+'?lang=he&context=1';d=json.load(urllib.request.urlopen(u,timeout=40));return dict(request=ref,url=u,**{k:d.get(k) for k in ['ref','sectionRef','sectionNames','sections','heVersionTitle','heVersionSource','heLicense','he','error']})
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:rs=list(ex.map(fetch,refs))
pathlib.Path('/tmp/KAB-002.context.json').write_text(json.dumps(rs,ensure_ascii=False))
for r in rs:print(r['request'],{k:r[k] for k in r if k!='he' and k!='url' and k!='request'})
