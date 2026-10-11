#!/usr/bin/env python3
"""Publish final finite-ledger YER-008 state transition."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def rows(p): return [json.loads(x) for x in (ROOT/p).read_text().splitlines() if x.strip()]
def save(p,x): (ROOT/p).write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in x))
tasks=rows('research/horse/state/tasks.jsonl')
for t in tasks:
 if t['id']=='YER-008':
  t['status']='done'; t['results']=['research/horse/yerushalmi/YER-008.build.py','research/horse/yerushalmi/YER-008.read-excerpts.json','research/horse/yerushalmi/YER-008.verdicts.jsonl','research/horse/yerushalmi/YER-008.sources.jsonl','research/horse/yerushalmi/YER-008.remaining.jsonl','research/horse/yerushalmi/YER-008.report.md']; t['updated_at']='2026-10-11'
save('research/horse/state/tasks.jsonl',tasks)
sources=rows('research/horse/data/sources.jsonl'); stats={'records':len(sources),'context_checked':sum(x['checks']['context_checked'] for x in sources),'independently_reviewed':sum(x['checks']['independent_reviewed'] for x in sources)}
p=ROOT/'research/horse/state/project.json'; project=json.loads(p.read_text()); project['pending_task_ids']=[x for x in project['pending_task_ids'] if x!='YER-008']; project['next_action']='Run final Bavli batch BAV-007; then finish COM-004 normalization and chronology before synthesis/comparison/audit.'; project['last_confirmed_commit']='14ff896f14acda0805ee713f3fc766cd4d248441'; project['registry_statistics']=stats; p.write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'research/horse/data/coverage.json'; coverage=json.loads(p.read_text())
for c in coverage['corpora']:
 if c['id']=='yerushalmi':
  c['confirmed_count']+=4; c['status']='processed'; c['limitations']=['Saved 149-candidate YER-002 discovery ledger is fully adjudicated, but this does not prove absolute completeness across every spelling, edition, commentary, manuscript or allusion.','Niddah mixed provenance/license and rare Makkot witness identification remain unresolved.']; c['next_checks']=['Independent review of central extraordinary/spiritual passages','Resolve edition/manuscript limitations if stronger completeness is required']
coverage['registry_statistics']=stats; coverage['checkpoint_note']='YER-008 read the final 9 named Yerushalmi candidates: 4 registered contexts, 5 lexical false positives, zero finite-ledger candidates remain; BAV 23 remain; COM-004 and chronology remain partial.'; p.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'research/horse/state/handoff.md'; s=p.read_text().replace('Последний подтверждённый предшествующий коммит: 16cec116b0ffed9d26535d860bd8f3139940f95c.','Последний подтверждённый предшествующий коммит: 14ff896f14acda0805ee713f3fc766cd4d248441.').replace('483 записи, 481 с проверенным контекстом','487 записей, 485 с проверенным контекстом').replace('YER-006 и YER-007 (ограниченные партии по 15)','YER-006, YER-007 и финальный YER-008').replace('YER-007 завершён: 3 контекста приняты, 12 лексических ложных совпадений отклонены; в конечной очереди Иерушалми осталось 9 кандидатов (`YER-008`).','YER-007 и YER-008 завершены; все 149 кандидатов сохранённого YER-002 ledger распределены, в финальной очереди Иерушалми осталось 0 кандидатов. Это не утверждение абсолютной полноты корпуса.').replace('Продолжать с финальным YER-008 или финальным BAV-007','Продолжать с финальным BAV-007')
p.write_text(s)
