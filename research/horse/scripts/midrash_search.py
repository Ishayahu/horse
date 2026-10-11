#!/usr/bin/env python3
"""Bounded source-only whitelist discovery; candidates are not manual verification."""
import concurrent.futures, hashlib, json, re, unicodedata, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'research/horse/midrash';OUT.mkdir(parents=True,exist_ok=True)
CACHE=Path('/tmp/horse-mid-cache');CACHE.mkdir(exist_ok=True)
TITLES=['Mekhilta DeRabbi Yishmael','Mekhilta DeRabbi Shimon Ben Yochai','Sifra','Sifrei Bamidbar','Sifrei Devarim','Bereshit Rabbah','Shemot Rabbah','Vayikra Rabbah','Bamidbar Rabbah','Devarim Rabbah','Midrash Tanchuma','Midrash Tanchuma Buber','Pesikta DeRav Kahana','Pesikta Rabbati','Midrash Tehillim','Midrash Mishlei','Pirkei DeRabbi Eliezer','Yalkut Shimoni on Torah','Yalkut Shimoni on Nach','Shir HaShirim Rabbah','Ruth Rabbah','Eikhah Rabbah','Esther Rabbah','Kohelet Rabbah','Aggadat Bereshit','Bereshit Rabbati','Midrash Aggadah','Midrash Shmuel','Mishnat Rabbi Eliezer','Otzar Midrashim','Tanna DeBei Eliyahu Rabbah','Tanna DeBei Eliyahu Zuta','Sefer HaYashar (midrash)','Midrash Tannaim on Deuteronomy','Sifrei Zuta']
def norm(s):
 return ''.join(c for c in unicodedata.normalize('NFD',re.sub('<[^>]+>','',s)) if not unicodedata.combining(c))
def leaves(obj,path=()):
 if isinstance(obj,str):yield path,obj
 elif isinstance(obj,list):
  for i,x in enumerate(obj):yield from leaves(x,path+(i+1,))
 elif isinstance(obj,dict):
  for k,x in obj.items():yield from leaves(x,path+(k,))
def scan(book):
 title=book['title'];url=book['json_url'];filename=CACHE/(re.sub('[^A-Za-z0-9]+','_',title)+'.json')
 try:
  if not filename.exists():filename.write_bytes(urllib.request.urlopen(url,timeout=40).read())
  raw=filename.read_bytes();data=json.loads(raw);rows=[];count=0
  for path,text in leaves(data['text']):
   if not text.strip():continue
   count+=1;n=norm(text);terms=[q for q in ['סוס','פרש','מרכב','רכב אש','לססתי'] if q in n]
   if not terms:continue
   first=min(n.index(q) for q in terms);start=max(0,first-150)
   rows.append({'id':'MID-002:'+title+':'+'.'.join(map(str,path)),'task_id':'MID-002','work':title,'export_path':list(path),'export_url':url,'excerpt_normalized':n[start:start+650],'excerpt_start':start,'full_segment_sha256':hashlib.sha256(text.encode()).hexdigest(),'excerpt_is_complete':len(n)<=start+650,'matched_terms':terms,'quote_machine_extracted':True,'context_checked':False,'locator_mapping_verified':False,'interpretation_prepared':False})
  metadata={k:v for k,v in data.items() if k not in ('text','versions')}
  return {'work':title,'status':'searched','url':url,'sha256':hashlib.sha256(raw).hexdigest(),'segments':count,'candidates':len(rows),'metadata':metadata},rows
 except Exception as e:return {'work':title,'status':'error','error':str(e),'url':url},[]
def main():
 index_url='https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/books.json'
 raw=urllib.request.urlopen(index_url,timeout=40).read();books=json.loads(raw)['books']
 selected=[b for b in books if b['title'] in TITLES and b['language']=='Hebrew' and b['versionTitle']=='merged']
 manifest={'schema_version':1,'task_id':'MID-002','inventory_url':index_url,'inventory_sha256':hashlib.sha256(raw).hexdigest(),'whitelist':TITLES,'works':[],'limitations':['Merged versions may combine editions; source locator and historical attribution require schema/manual validation.','Full exports cached outside repository; brief original excerpts only.','Substring search generates false positives; no completeness claim for synonyms or motifs.']}
 candidates=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for entry,rows in pool.map(scan,selected):
   manifest['works'].append(entry);candidates.extend(rows)
   (OUT/'MID-002.manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
   (OUT/'MID-002.candidates.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in candidates))
   print(entry['work'],entry['status'],entry.get('candidates'),flush=True)
 print('TOTAL',len(selected),len(candidates),flush=True)
if __name__=='__main__':main()
