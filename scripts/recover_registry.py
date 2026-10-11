#!/usr/bin/env python3
"""Additive integration of recovered task outputs; coordinator-only local operation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(path):
 return [json.loads(s) for s in (ROOT/path).read_text().splitlines() if s.strip()]
def save(path,value):
 (ROOT/path).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in value))
def main():
 by={s['id']:s for s in rows('data/sources.jsonl')}
 batches=['research/tanakh/TAN-002b.sources.jsonl','research/midrash/MID-004.sources.jsonl','research/egypt/EGY-001.sources.jsonl','research/kabbalah/KAB-002.sources.jsonl','research/later-literature/LAT-002.sources.jsonl','research/tanakh/TAN-003.sources.jsonl','research/commentaries/COM-002.sources.jsonl','research/perek-shira/PSH-002.sources.jsonl','research/tanakh/TAN-004.sources.jsonl','research/commentaries/COM-003.sources.jsonl','research/commentaries/COM-004.sources.jsonl','research/bavli/BAV-003.sources.jsonl','research/bavli/BAV-004.sources.jsonl','research/bavli/BAV-005.sources.jsonl','research/bavli/BAV-006.sources.jsonl','research/bavli/BAV-007.sources.jsonl','research/yerushalmi/YER-004.sources.jsonl','research/yerushalmi/YER-005.sources.jsonl','research/yerushalmi/YER-006.sources.jsonl','research/yerushalmi/YER-007.sources.jsonl','research/yerushalmi/YER-008.sources.jsonl','research/egypt/EGY-002.sources.jsonl']
 for path in batches:
  if not (ROOT/path).exists():continue
  for s in rows(path):by[s['id']]=s
 for s in by.values():
  if s.get('parent_source_id') and s['parent_source_id'] not in by:
   s['parent_reference']=s['parent_source_id'];s['parent_source_id']=None
  s.setdefault('period_status','Historical composition/edition dating not independently established')
  s.setdefault('confidence',{'quotation':'verified_in_named_digital_witness' if s['checks']['quote_verified'] else 'not_verified','interpretation':'working_contextual_reading' if s['checks']['interpretation_prepared'] else 'not_prepared'})
 for path in sorted((ROOT/'research/verification').glob('*.jsonl')):
  for line in path.read_text().splitlines():
   if not line.strip():continue
   v=json.loads(line);sid=v.get('source_id')
   if sid not in by:continue
   reviewer=v.get('independent_reviewer') or v.get('reviewer')
   if not reviewer:continue
   s=by[sid];s['reviewers']=list(dict.fromkeys(s['reviewers']+[reviewer]));s['checks']['independent_reviewed']=True
   note=v.get('correction') or v.get('finding');notes=s.setdefault('verification_notes',[])
   if note and note not in notes:notes.append(note)
   patch=v.get('suggested_source_patch')
   if isinstance(patch,dict):
    for key,value in patch.items():s[key]=value
   if isinstance(note,dict):
    if note.get('locator'):s['locator']=note['locator']
    if note.get('url'):s.setdefault('initial_url',s['url']);s['url']=note['url']
    if note.get('quote_suggestion'):s['quote_context_addition']=note['quote_suggestion']
 save('data/sources.jsonl',list(by.values()))
 print(json.dumps({'records':len(by),'context_checked':sum(s['checks']['context_checked'] for s in by.values()),'independently_reviewed':sum(s['checks']['independent_reviewed'] for s in by.values())}))
if __name__=='__main__':main()
