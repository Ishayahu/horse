#!/usr/bin/env python3
"""Reproducible OSHB WLC Tanakh horse inventory. Stdlib only; corpus cache outside git."""
import concurrent.futures,datetime,hashlib,json,pathlib,re,urllib.request,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[3]; OUT=ROOT/'research/tanakh'; CACHE=pathlib.Path('/tmp/horse-oshb-wlc');CACHE.mkdir(exist_ok=True)
REVISION='3d15126fb1ef74867fc1434be1942e837932691f'
BOOKS='Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal'.split()
NS={'o':'http://www.bibletechnologies.net/2003/OSIS/namespace'}
def norm(t):return ''.join(c for c in t if not ('\u0591'<=c<='\u05c7') and c!='/')
def fetch(book):
 u=f'https://raw.githubusercontent.com/openscriptures/morphhb/{REVISION}/wlc/{book}.xml';p=CACHE/f'{REVISION}-{book}.xml'
 if not p.exists():p.write_bytes(urllib.request.urlopen(u,timeout=90).read())
 return book,u,p.read_bytes()
def row(book,url,v,words,hits,kind):
 ref=v.attrib['osisID'];quote=' '.join(''.join(w.itertext()).replace('/','') for w in words)
 return {'id':'tanakh-wlc-'+ref.lower().replace('.','-')+('' if kind=='direct' else '-candidate'),'corpus_id':'tanakh','work':book,'locator':ref,'url':url,'edition':'Open Scriptures Hebrew Bible / Westminster Leningrad Codex XML','language':'he','mention_type':kind,'parent_source_id':None,'quote':quote,'quote_format':'XML w-token transcription, with slash morpheme separators removed and spaces inserted; both ketiv and qere retained where XML contains both.','context':'Complete verse supplied; adjacent verse context is present in downloaded chapter and has not been manually reviewed.','checks':{'primary_read':True,'quote_verified':True,'context_checked':False,'attribution_verified':True,'commentaries_checked':False,'interpretation_prepared':False,'independent_reviewed':False},'interpretation':None,'epistemic_type':'direct_text','reviewers':['TAN-001 programmatic XML extraction'],'task_id':'TAN-001','limitations':['Verse and lexemes machine extracted; role and narrative context require human review.'],'accessed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'matched_tokens':hits,'categories':['horse_lexeme' if kind=='direct' else 'rider_chariot_abir_candidate'],'role':'unclassified'}
def main():
 OUT.mkdir(parents=True,exist_ok=True);direct=[];indirect=[];amb=[];manifest=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:corpora=list(ex.map(fetch,BOOKS))
 for book,url,data in corpora:
  root=ET.fromstring(data);vs=root.findall('.//o:verse',NS);manifest.append({'book':book,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'verses':len(vs),'download_http_status':200})
  for v in vs:
   words=v.findall('.//o:w',NS);horse=[];other=[];unclear=[]
   for w in words:
    t=''.join(w.itertext());lem=w.attrib.get('lemma','');n=norm(t);hit={'hebrew':t.replace('/',''),'word_id':w.attrib.get('id'),'type':w.attrib.get('type'),'normalized':n,'lemma':lem,'morph':w.attrib.get('morph')}
    if re.search(r'(?<!\d)548[34](?!\d)',lem):
     # OSHB 5483 a = swallow; 5483 b = horse; 5484 = mare.
     (unclear if '5483 a' in lem else horse).append(hit)
    elif 'סוס' in n:unclear.append(hit)
    if re.search(r'(?<!\d)(6571|7392|7393|7398|7399|7400|47)(?!\d)',lem):other.append(hit)
   if horse:direct.append(row(book,url,v,words,horse,'direct'))
   if other:indirect.append(row(book,url,v,words,other,'indirect'))
   if unclear:
    ar=row(book,url,v,words,unclear,'indirect');ar['id']=ar['id'].removesuffix('-candidate')+'-ambiguity';ar['categories']=['lexical_false_positive'];ar['role']='name_or_bird_not_horse';amb.append(ar)
 for name,rows in [('direct',direct),('indirect-candidates',indirect),('ambiguities',amb)]:
  (OUT/f'TAN-001.{name}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
 (OUT/'TAN-001.manifest.json').write_text(json.dumps({'schema_version':1,'revision':REVISION,'attribution':'Open Scriptures Hebrew Bible Project; morphology CC BY 4.0, WLC text public domain (repository README).','corpus':'OSHB WLC 39 XML books','retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'query':'Strong 5483 b + 5484; normalized substring סוס fallback; separate lexemes 6571,7392,7393,7398,7399,7400,47','books':manifest,'counts':{'direct_verses':len(direct),'direct_tokens':sum(len(r['matched_tokens']) for r in direct),'indirect_candidate_verses':len(indirect),'ambiguity_verses':len(amb)}},ensure_ascii=False,indent=2))
 print(json.dumps({'direct':len(direct),'indirect':len(indirect),'ambiguous':len(amb)}))
if __name__=='__main__':main()
