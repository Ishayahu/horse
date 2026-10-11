"""Reproduce bounded lexical discovery without persisting full exported corpus.
Fetch Sefaria per-tractate merged Hebrew JSON in memory; never redistribute it.
Input inventory records the October 2026 download URLs. Outputs discovery rows,
not verified source assertions. Source records require human context reading.
"""
import json,re,unicodedata,urllib.request,pathlib,hashlib
ROOT=pathlib.Path(__file__).parent
inv=json.loads((ROOT/'BAV-001.inventory.json').read_text())
def normalize(s):
    return ''.join(c for c in re.sub('<[^>]+>','',s) if not unicodedata.combining(c))
rows=[]
for x in inv['selected']:
    d=json.load(urllib.request.urlopen(x['json_url'],timeout=60))
    assert d['sectionNames']==['Daf','Line']
    assert d['text'][0:2]==[[],[]], 'Mapping requires leading 1a/1b empty slots'
    for idx,ss in enumerate(d['text']):
        for n,s in enumerate(ss):
            c=normalize(s)
            if re.search('סוס|פרש',c):
                rows.append({'work':x['title'],'locator':str((idx+2)//2)+('a' if (idx+2)%2==0 else 'b')+':'+str(n+1),'matched_query':'סוס' if 'סוס' in c else 'פרש','disposition':'equine_candidate' if 'סוס' in c or re.search('פרשיו|פרשים',c) else 'excluded_non_equine_root','excerpt':c[:220],'primary_url':x['json_url'],'task_id':'BAV-001'})
(ROOT/'BAV-001.candidates.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
print('candidate segments',len(rows),'equine',sum(x['disposition']=='equine_candidate' for x in rows))
