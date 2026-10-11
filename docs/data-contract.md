# Форматы v1
UTF-8; JSONL = один объект на строку; пустой файл = пустой реестр. schema_version=1 в JSON.
tasks: id, codename, goal, corpus, queries[], depends_on[], expected_output, completion_criteria, status (pending/running/partial/blocked/done), results[], limitations[], open_questions[], assignment (null либо {session_id,worker_id,started_at}), updated_at.
sources: id (нормализованный work+locator+commentator/version), corpus_id, work, locator, url, edition, language, mention_type (direct/indirect), parent_source_id, quote, context, checks {primary_read,quote_verified,context_checked,attribution_verified,commentaries_checked,interpretation_prepared,independent_reviewed}, interpretation, epistemic_type, reviewers[], task_id, limitations[], accessed_at. checks — независимые признаки, не автоматически возрастающий статус.
references: id, source_id, target_source_id, relation, evidence, epistemic_type.
coverage: corpora[]; каждый {id,works[],status,queries[],ranges[],candidate_count,confirmed_count,commentary_count,limitations[],next_checks[]}. Счётчики исходно нулевые, статус not_started.
project: phase, current_assignment (null либо цель+идентификатор+хэш исходного задания), session_id, active_task_ids[], pending_task_ids[], unsaved_results[], blockers[], next_action, last_confirmed_commit, capabilities.
hypotheses.jsonl: id, claim, epistemic_type, source_ids[], mechanism, falsifiers[], alternatives[], confidence, followup_task_ids[].
decisions.jsonl: id,date,decision,rationale,task_ids[].
handoff — короткое человекочитаемое отражение состояния. Проверка валидатором обязательна перед checkpoint. Running из прошлого сеанса не означает выполненное.

## Тематическое размещение итоговых результатов

Конечные проверенные каталоги, отчёты и аудиты помещаются по одной теме в `reports/<research-slug>/`. В корне `reports/` разрешён только общий указатель. `HORSE-RESEARCH-001` и `HORSE-SUPPLEMENT-001` публикуются в `reports/horse/`; `YIRAT-RESEARCH-001` — в `reports/yirat-shamayim/`. Задания `tasks.jsonl` и код генерации должны ссылаться на фактические пути; исторические статусы не менять при чисто структурном переносе.

## Обязательное поле `codename` и пути артефактов

Каждое исследовательское задание/подзадача (`tasks.jsonl`) имеет строковое `codename`, отдельное от `id` и строго равное basename обеих папок `research/<codename>/` и `reports/<codename>/`. Требование действует для очереди исследований и записей каждого тематического `tasks.jsonl`. Вновь создаваемые результаты и состояния допускаются только внутри соответствующей темы. Схема: `codename: "horse"` для HORSE и supplement, `codename: "yirat-shamayim"` для YIRAT. Корни `research/` и `reports/` — только указатели; общая координационная методология может оставаться в корне репозитория. Исторические данные HORSE хранятся в `research/horse/data/` и `research/horse/state/`; первичные корпусные файлы и проверки — в остальных папках `research/horse/`. Не создавать новые глобальные реестры для конкретной темы; `id`, `codename`, ссылки и история должны быть сохранены.
