#!/usr/bin/env python3
"""Pinned TAN-003 lexeme inventory and reviewed decisions. Stdlib; no root substring matching."""
import json,re,hashlib,xml.etree.ElementTree as ET
import tanakh_search as t
OUT=t.OUT
LEX={'46','47','4817','4818','7392','7393','7395','7396','7398','7409','6571 b'}
def lemmas(s):return re.findall(r'(?<!\d)\d+(?: [ab])?(?!\d)',s)
def inventory():
 rows=[];manifest=[]
 for book in t.BOOKS:
  _,url,data=t.fetch(book);manifest.append({'book':book,'url':url,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
  expected={x['book']:x['sha256'] for x in json.loads((OUT/'TAN-001.manifest.json').read_text())['books']}
  if hashlib.sha256(data).hexdigest()!=expected[book]:raise ValueError('Pinned corpus hash mismatch: '+book)
  root=ET.fromstring(data)
  for ch in root.findall('.//o:chapter',t.NS):
   vs=ch.findall('.//o:verse',t.NS)
   for i,v in enumerate(vs):
    ws=v.findall('.//o:w',t.NS);hits=[]
    for w in ws:
     if set(lemmas(w.get('lemma','')))&LEX:hits.append({'hebrew':''.join(w.itertext()).replace('/',''),'lemma':w.get('lemma'),'morph':w.get('morph'),'word_id':w.get('id')})
    if not hits:continue
    row=t.row(book,url,v,ws,hits,'indirect');row['task_id']='TAN-003';row['id']=row['id'].removesuffix('-candidate')+'-indirect'
    row['context_quotes']=[{'locator':x.get('osisID'),'quote':' '.join(''.join(w.itertext()).replace('/','') for w in x.findall('.//o:w',t.NS))} for x in vs[max(0,i-1):i+2]]
    row['context_refs']=[x['locator'] for x in row['context_quotes']];rows.append(row)
 return rows,manifest
def main():
 rows,books=inventory();old={r['locator']:r for name in ['TAN-002a.sources.jsonl','TAN-002b.sources.jsonl'] for r in map(json.loads,(OUT/name).read_text().splitlines())};decpath=OUT/'TAN-003.decisions.jsonl';dec={r['locator']:r for r in map(json.loads,decpath.read_text().splitlines())} if decpath.exists() else {};sources=[];audit=[]
 for r in rows:
  loc=r['locator'];d=dec.get(loc)
  if loc in old:status='already_reviewed';reason='Existing TAN-002a/b context-reviewed source; no duplicate emitted. '+(old[loc].get('interpretation') or old[loc]['context']);sid=old[loc]['id']
  elif d:
   status=d['status'];reason=d['reason'];sid=r['id'] if status=='accepted' else None
   if status=='accepted':
    r.update(context=d['context'],interpretation=d['reason'],role=d['role'],categories=d['categories'],reviewers=['TAN-003 Hebrew verse and stored adjacent context review'],limitations=['Horse inferred from riding/chariot context unless רכש; chariot itself does not prove explicit horse token. Commentaries and independent review not performed.'])
    r['checks'].update(context_checked=True,interpretation_prepared=True);sources.append(r)
  else:status='pending';reason='Not yet context reviewed.';sid=None
  audit.append({'locator':loc,'status':status,'reason':reason,'source_id':sid,'matched_tokens':r['matched_tokens'],'context_refs':r['context_refs']})
 raw=[json.loads(x) for x in (OUT/'TAN-001.indirect-candidates.jsonl').read_text().splitlines()];current={r['locator'] for r in rows};delta=[{'locator':r['locator'],'status':'retained_by_corrected_query' if r['locator'] in current else 'excluded_from_corrected_query','reason':'At least one corrected lemma hit.' if r['locator'] in current else 'Original query matches only excluded lexeme families (property רכוש 7399, gossip רכיל 7400, or non-cavalry 6571 a); excluded as detection hits, not a claim about every possible context.','old_matched_tokens':r['matched_tokens']} for r in raw]
 for name,x in [('query-delta',delta),('candidates',rows),('audit',audit),('sources',sources)]: (OUT/f'TAN-003.{name}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in x))
 (OUT/'TAN-003.manifest.json').write_text(json.dumps({'schema_version':1,'revision':t.REVISION,'scope':'Exact OSHB lemma IDs: '+','.join(sorted(LEX))+'; all morphology codes retained, no morph restriction; 6571 a excluded; 46 ambiguous separate candidate family.','books':books,'counts':{s:sum(r['status']==s for r in audit) for s in ['already_reviewed','accepted','rejected','pending']}},ensure_ascii=False,indent=2))
 print(len(rows),{s:sum(r['status']==s for r in audit) for s in ['already_reviewed','accepted','rejected','pending']})
if __name__=='__main__':main()
