#!/usr/bin/env python3
"""YER-002 bounded complete-index discovery, stdlib. Corpus cache outside repository."""
import concurrent.futures,datetime,hashlib,html,json,pathlib,re,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=ROOT/'research/yerushalmi';CACHE=pathlib.Path('/tmp/horse-yerushalmi-export');CACHE.mkdir(exist_ok=True)
INDEX_URL='https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/books.json'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(u):
 p=CACHE/(hashlib.sha256(u.encode()).hexdigest()+'.json')
 if not p.exists():
  b=urllib.request.urlopen(u,timeout=55).read();p.write_bytes(b)
 return p.read_bytes()
def norm(s):return re.sub('[\u0591-\u05c7]','',s)
def clean(s):return html.unescape(re.sub('<[^>]*>','',s))
def leaves(v,path=()):
 if isinstance(v,list):
  for i,x in enumerate(v,1):yield from leaves(x,path+(i,))
 elif isinstance(v,str):yield path,v
 elif v is not None:raise ValueError('Non-string leaf')
def work(e):
 title=e['title'];url=e['json_url'];m={'work':title,'url':url,'accessed_at':NOW,'status':'error'}
 try:
  raw=fetch(url);d=json.loads(raw);idx_url='https://www.sefaria.org/api/v2/raw/index/'+urllib.parse.quote(title.replace(' ','_'));ix=json.loads(fetch(idx_url));s=ix['schema']
  if s.get('nodes') or s.get('depth')!=3 or s.get('addressTypes')!=['Perek','Halakhah','Integer']:raise ValueError('Unrecognized schema: refuse invented locator')
  ll=list(leaves(d['text']));valid=all(len(path)==3 for path,_ in ll)
  if not valid:raise ValueError('Leaf depth differs from schema')
  meta_url='https://www.sefaria.org/api/texts/'+urllib.parse.quote(title.replace(' ','_')+'.1.1')+'?context=0'
  try:
   meta=json.loads(fetch(meta_url));licenses=[{'versionTitle':x.get('versionTitle'),'license':x.get('license'),'language':x.get('language')} for x in meta.get('versions',[]) if x.get('language')=='he'];license_err=None
  except Exception as ex:licenses=[];license_err=str(ex)
  m.update(status='searched',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),edition=d.get('versionTitle'),versions=d.get('versions'),versionSource=d.get('versionSource'),license=d.get('license'),license_metadata=licenses,license_error=license_err,index_url=idx_url,schema=s,sectionNames=d.get('sectionNames'),segment_count=len(ll),nonempty_segments=sum(bool(clean(t).strip()) for _,t in ll),completeness='All string leaves of this retrieved merged export traversed; historical/textual completeness not asserted')
  rows=[]
  for path,t in ll:
   text=clean(t);tokens=re.findall('[א-ת]+',norm(text));hits=[]
   for token in tokens:
    kinds=[]
    if 'סוס' in token:
     kinds.append('horse_substring')
     if re.fullmatch('[ובכלמשהד]*סוס(?:ים|ין|יא|ייא|יי|י|ו|ה|ת|תא|תי|תו|תה|ות|יהם|יהן|יכם|יכן|ינו|יך|ך|כם|כן|הון|הין)?',token):kinds.append('horse_morphological_form')
    if re.fullmatch('[ובכלמשה]*פרש(?:ים|ין|יא|ייא|א)?',token):kinds.append('rider_ambiguous')
    if any(x in token for x in ['מרכב','אורוו','אוריו','אספסט','היפוס']):kinds.append('chariot_stable_loanword_ambiguous')
    if kinds:hits.append({'token':token,'classes':kinds})
   if not hits:continue
   loc=':'.join(map(str,path));ref=title+' '+loc;slug=title.replace(' ','_')+'.'+loc.replace(':','.')
   rows.append({'id':'yer-002-'+slug.lower().replace('_','-').replace('.','-'),'task_id':'YER-002','corpus_id':'yerushalmi','work':title,'locator':loc,'url':'https://www.sefaria.org/'+slug,'export_url':url,'edition':'Sefaria merged Hebrew export','constituent_versions':d.get('versions'),'matched_tokens':hits,'quote':text,'quote_format':'Original full segment with HTML tags removed/entities decoded; pointing preserved','checks':{'primary_read':False,'quote_verified':False,'context_checked':False,'attribution_verified':False,'commentaries_checked':False,'interpretation_prepared':False,'independent_reviewed':False},'discovery_status':'machine_extracted_candidate','accessed_at':NOW,'already_verified_YER001':title=='Jerusalem Talmud Sanhedrin' and loc in ['2:6:1','2:6:3','2:6:5','2:6:11','6:1:1'],'limitations':['Machine match; horse meaning, source attribution, context and quotation require human review.','Merged export version provenance not per-segment resolved.']})
  m['candidate_count']=len(rows);return m,rows
 except Exception as ex:m['error']=repr(ex);return m,[]
def save(man,rows):
 for name,obj in [('manifest.json',man),('candidates.jsonl',rows)]:
  p=OUT/('YER-002.'+name);q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(obj,ensure_ascii=False,indent=2) if name.endswith('.json') else ''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in obj));q.replace(p)
def main():
 OUT.mkdir(parents=True,exist_ok=True);b=fetch(INDEX_URL);index=json.loads(b);entries=[e for e in index['books'] if e['title'].startswith('Jerusalem Talmud ') and e['language']=='Hebrew' and e['versionTitle']=='merged' and e['categories'][:2]==['Talmud','Yerushalmi']]
 man={'schema_version':1,'task_id':'YER-002','index_url':INDEX_URL,'index_sha256':hashlib.sha256(b).hexdigest(),'index_generated_at':index.get('generated_at'),'started_at':NOW,'inventory_count':len(entries),'inventory':[{'title':e['title'],'url':e['json_url']} for e in entries],'queries':['Normalized Hebrew token containing סוס (covers prefixed/suffixed סוסים סוסין סוסיא סוסייא סוסתא)','Prefix-bounded פרש/פרשים/פרשין/פרשיא/פרשייא/פרשא ambiguous','Substring מרכב אורוו אוריו אספסט היפוס ambiguous'],'license_policy':'No corpus dump committed. Sefaria LICENSE.md: each version licensed independently. Missing export license recorded; API version metadata supplementary.','works':[],'status':'running'};rows=[];save(man,rows)
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
  fs=[ex.submit(work,e) for e in entries]
  for f in concurrent.futures.as_completed(fs):
   m,rr=f.result();man['works'].append(m);rows.extend(rr);save(man,rows);print(m['work'],m['status'],len(rr),flush=True)
 man['counts']={'searched_works':sum(x['status']=='searched' for x in man['works']),'errors':sum(x['status']=='error' for x in man['works']),'segments':sum(x.get('segment_count',0) for x in man['works']),'candidate_segments':len(rows),'horse_substring_segments':sum(any('horse_substring' in h['classes'] for h in r['matched_tokens']) for r in rows),'horse_form_segments':sum(any('horse_morphological_form' in h['classes'] for h in r['matched_tokens']) for r in rows),'reused_YER001':sum(r['already_verified_YER001'] for r in rows)};man['status']='done' if man['counts']['errors']==0 else 'partial';man['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();man['works'].sort(key=lambda x:x['work']);rows.sort(key=lambda x:(x['work'],[int(n) for n in x['locator'].split(':')]));save(man,rows);print(json.dumps(man['counts']))
if __name__=='__main__':main()
