"""Finite discovery scan: remaining 34 canonical Bavli tractates. No corpus cache.
Requires BAV-001.inventory.json whitelist. Candidate excerpts are discovery only.
"""
import json,re,unicodedata,urllib.request,pathlib,hashlib,concurrent.futures,datetime
ROOT=pathlib.Path(__file__).parent
inventory=json.loads((ROOT/'BAV-001.inventory.json').read_text())
selected=[x for x in inventory['base_tractates'] if x['title'] not in {'Berakhot','Pesachim','Sanhedrin'}]
queries=['סוס','פרש','רכב','פרד','סייח','רכש','אביר','אצטבל','איצטבל','אורווה','ארוות']
def clean(s):return ''.join(c for c in re.sub('<[^>]+>','',s) if not unicodedata.combining(c))
def scan(x):
    try:
        raw=urllib.request.urlopen(x['url'],timeout=80).read(); d=json.loads(raw)
        assert d['sectionNames']==['Daf','Line']
        assert d['text'][:2]==[[],[]]
        cs=[]
        for idx,segs in enumerate(d['text']):
            for n,s in enumerate(segs):
                c=clean(s); hits=[q for q in queries if q in c]
                if hits:
                    loc=str((idx+2)//2)+('a' if (idx+2)%2==0 else 'b')+':'+str(n+1)
                    disposition='explicit_horse_candidate' if 'סוס' in hits else 'adjacent_species_candidate' if any(q in hits for q in ['פרד','סייח','רכש']) else 'broad_root_needs_filter'
                    cs.append({'work':x['title'],'locator':loc,'url':x['url'],'queries':hits,'disposition':disposition,'excerpt':c[:200],'task_id':'BAV-002','checks':{'primary_downloaded':True,'context_checked':False,'quote_verified':False,'independent_reviewed':False}})
        meta={'work':x['title'],'url':x['url'],'status':'scanned','transport_sha256':hashlib.sha256(raw).hexdigest(),'range':'2a–'+str(len(d['text'])//2)+('a' if len(d['text'])%2 else 'b'),'array_slots':len(d['text']),'nonempty_amudim':sum(bool(s) for s in d['text']),'candidate_segments':len(cs),'horse_candidate_segments':sum(c['disposition']=='explicit_horse_candidate' for c in cs),'edition_versions':d.get('versions'),'license':d.get('license'),'license_note':'No top-level license field present; individual version rights not inferred.' if 'license' not in d else 'License from downloaded JSON.'}
        return meta,cs
    except Exception as e:return {'work':x['title'],'url':x['url'],'status':'unavailable','error':str(e)},[]
metas=[]; candidates=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for meta,cs in pool.map(scan,selected):
        metas.append(meta);candidates.extend(cs);print(meta['work'],meta['status'],meta.get('candidate_segments'),flush=True)
raw_horse_count=sum(c['disposition']=='explicit_horse_candidate' for c in candidates)
for c in candidates:
    if c['disposition']=='explicit_horse_candidate' and any(q in c['excerpt'] for q in ['דוכסוס','קיסוס','סוסביל','סוסכינת']):
        c['disposition']='excluded_non_equine_substring'
        c['exclusion_reason']='Lexical compound: parchment/ivy/locust/disease, not horse.'
summary={'schema_version':1,'task_id':'BAV-002','reviewer':'/root/bavli','accessed_at':'2026-10-09','queries':queries,'scope':'34 canonical tractates excluding BAV-001 three; discovery only','works':metas,'candidate_count':len(candidates),'raw_horse_substring_count':raw_horse_count,'excluded_false_horse_substring_count':sum(c['disposition']=='excluded_non_equine_substring' for c in candidates),'explicit_horse_candidate_count':sum(c['disposition']=='explicit_horse_candidate' for c in candidates),'context_verified_sources':0,'full_corpus_persisted':False}
(ROOT/'BAV-002.inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
(ROOT/'BAV-002.candidates.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in candidates))
print('DONE',len(metas),'candidates',len(candidates),'horse',summary['explicit_horse_candidate_count'],flush=True)
