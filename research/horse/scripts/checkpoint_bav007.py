#!/usr/bin/env python3
"""Publish final finite-ledger BAV-007 state transition."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def rows(p): return [json.loads(x) for x in (ROOT/p).read_text().splitlines() if x.strip()]
def save(p,x): (ROOT/p).write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in x))
tasks=rows('research/horse/state/tasks.jsonl')
for t in tasks:
 if t['id']=='BAV-007':
  t['status']='done'; t['results']=['research/horse/bavli/BAV-007.fetch.py','research/horse/bavli/BAV-007.build.py','research/horse/bavli/BAV-007.read-excerpts.json','research/horse/bavli/BAV-007.verdicts.jsonl','research/horse/bavli/BAV-007.sources.jsonl','research/horse/bavli/BAV-007.remaining.jsonl','research/horse/bavli/BAV-007.report.md']; t['limitations']=['Saved finite discovery ledger fully adjudicated; live adjacent-segment API retrieval timed out, so final batch context scope is the complete saved target segment.','Finite-ledger completion does not establish absolute completeness of every spelling, edition, commentary or manuscript.']; t['updated_at']='2026-10-11'
save('research/horse/state/tasks.jsonl',tasks)
sources=rows('research/horse/data/sources.jsonl'); stats={'records':len(sources),'context_checked':sum(x['checks']['context_checked'] for x in sources),'independently_reviewed':sum(x['checks']['independent_reviewed'] for x in sources)}
p=ROOT/'research/horse/state/project.json'; project=json.loads(p.read_text()); project['pending_task_ids']=[x for x in project['pending_task_ids'] if x!='BAV-007']; project['next_action']='Finish COM-004 normalization and chronology (CHR-001/CHR-002), then resolve remaining KAB-002 status before synthesis/comparison/audit.'; project['last_confirmed_commit']='9bf0cf3b828b0ce3604470cde558b82cd68567ff'; project['registry_statistics']=stats; p.write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'research/horse/data/coverage.json'; coverage=json.loads(p.read_text())
for c in coverage['corpora']:
 if c['id']=='bavli':
  c['confirmed_count']+=21; c['status']='processed'; c['limitations']=['Saved BAV-002 finite discovery ledger is fully adjudicated, but this does not prove absolute completeness across every spelling, edition, commentary, manuscript or allusion.','The final 23-candidate pass used complete saved target segments because live adjacent-segment API retrieval timed out; earlier batches include bounded adjacent context.']; c['next_checks']=['Independent review of central extraordinary/spiritual passages','Resolve edition/manuscript limitations if stronger completeness is required']
coverage['registry_statistics']=stats; coverage['checkpoint_note']='BAV-007 adjudicated the final 23 saved Bavli candidates: 21 registered contexts, 2 covered continuations/repeats, zero finite-ledger candidates remain; Yerushalmi ledger also has zero remaining. COM-004 and chronology remain partial.'; p.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'research/horse/state/handoff.md'; s=p.read_text().replace('Последний подтверждённый предшествующий коммит: 14ff896f14acda0805ee713f3fc766cd4d248441.','Последний подтверждённый предшествующий коммит: 9bf0cf3b828b0ce3604470cde558b82cd68567ff.').replace('487 записей, 485 с проверенным контекстом','508 записей, 506 с проверенным контекстом').replace('BAV-006 завершён: из 20 кандидатов 15 зарегистрированы отдельно, 5 оказались уже прочитанными продолжениями; в конечной очереди Бавли осталось 23 кандидата (`BAV-007`).','BAV-006 и финальный BAV-007 завершены; все кандидаты сохранённого BAV-002 ledger распределены, в конечной очереди Бавли осталось 0. Последняя партия дала 21 контекст и 2 уже покрытых продолжения/повтора; это не утверждение абсолютной полноты корпуса.').replace('Продолжать с финальным BAV-007, затем нормализовать COM-004 и добрать хронологию.','Продолжать с нормализации COM-004 и хронологии CHR-001/CHR-002, затем сверить KAB-002 перед синтезом.')
p.write_text(s)
