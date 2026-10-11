#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rows(p): return [json.loads(x) for x in (R/p).read_text().splitlines() if x.strip()]
def save(p,x): (R/p).write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in x))
t=rows('state/tasks.jsonl')
for x in t:
 if x['id']=='COM-004': x['status']='done'; x['results']=['research/commentaries/COM-004.fetch.py','research/commentaries/COM-004.build.py','research/commentaries/COM-004.coverage.json','research/commentaries/COM-004.discoveries.jsonl','research/commentaries/COM-004.manifest.json','research/commentaries/COM-004.sources.jsonl','research/commentaries/COM-004.report.md']; x['updated_at']='2026-10-11'
save('state/tasks.jsonl',t)
s=rows('data/sources.jsonl'); stats={'records':len(s),'context_checked':sum(x['checks']['context_checked'] for x in s),'independently_reviewed':sum(x['checks']['independent_reviewed'] for x in s)}
p=R/'state/project.json'; q=json.loads(p.read_text()); q['pending_task_ids']=[x for x in q['pending_task_ids'] if x!='COM-004']; q['next_action']='Finish chronology CHR-001/CHR-002, then resolve KAB-002 status before synthesis/comparison/audit.'; q['last_confirmed_commit']='b0f1b2d39f21a7fe24131d96ac01de5a69afc192'; q['registry_statistics']=stats; p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
p=R/'data/coverage.json'; c=json.loads(p.read_text())
for x in c['corpora']:
 if x['id']=='commentaries': x['confirmed_count']=29; x['candidate_count']=max(x['candidate_count'],29); x['limitations']=['COM-004 finite matrix normalized; missing indexed titles and empty exact verse cells do not establish absence from print or grouped commentary.','Default digital Hebrew responses are not print/manuscript collation; most selected commentary remains without independent review.']; x['next_checks']=['Independent review of Abarbanel/Ibn Ezra central Zechariah interpretations','Broader authors and print witnesses only if required by final audit']
c['registry_statistics']=stats; c['checkpoint_note']='COM-004 normalized 16 meaningful Abarbanel/Ibn Ezra Zechariah commentary cells; Bavli and Yerushalmi finite ledgers remain closed; chronology remains partial.'; p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
p=R/'state/handoff.md'; z=p.read_text().replace('Последний подтверждённый предшествующий коммит: 9bf0cf3b828b0ce3604470cde558b82cd68567ff.','Последний подтверждённый предшествующий коммит: b0f1b2d39f21a7fe24131d96ac01de5a69afc192.').replace('508 записей, 506 с проверенным контекстом','524 записи, 522 с проверенным контекстом').replace('COM-004 и CHR-002 имеют полезные артефакты, но остаются partial.','COM-004 завершён: нормализованы 16 содержательных ячеек Абарбанеля и Ибн Эзры по видениям Захарии. CHR-001/CHR-002 остаются partial.').replace('Продолжать с нормализации COM-004 и хронологии CHR-001/CHR-002, затем сверить KAB-002 перед синтезом.','Продолжать с хронологии CHR-001/CHR-002, затем сверить KAB-002 перед синтезом.')
p.write_text(z)
