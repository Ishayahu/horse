# horse — промежуточные материалы исследования коней

**`codename: horse`** · Основная тема: `HORSE-RESEARCH-001` (завершено в ограниченном охвате), дополнительная проверка: `HORSE-SUPPLEMENT-001` (в работе). Итоговые читательские материалы: [`reports/horse/`](../../reports/horse/).

## Временная карта уже существующих материалов

До безопасной атомарной миграции исторический корпус HORSE фактически расположен в:

- `research/tanakh/`, `research/bavli/`, `research/yerushalmi/`, `research/midrash/`, `research/commentaries/`, `research/later-literature/`;
- `research/kabbalah/`, `research/perek-shira/`, `research/comparative/`, `research/egypt/`, `research/provenance/`, `research/verification/`;
- `research/horse-supplement/` — текущие промежуточные результаты дополнительного исследования;
- `data/` (старый реестр и покрытие) и `state/` (задачи/checkpoint исходного HORSE).

Все эти папки **относятся только к codename `horse`**, а не к другим исследованиям. Наличие старых папок пока означает неполную физическую миграцию, не другой `codename`. Не дублировать реестр и не переписывать исходные цитаты ради перемещения.

**Требуемое целевое расположение:** `research/horse/<corpus>/...`, `research/horse/supplement/...`, `research/horse/data/...` и `research/horse/state/...`. Перенос должен сохранить историю и работоспособность, исправить все JSONL/Markdown/Python пути и ссылки, а затем проверить удалённый checkpoint. До такого переноса исторические артефакты продолжают читаться по фактическим адресам.

[Методология](../../docs/methodology.md) · [Очередь](../../RESEARCH-RUNNER.md).
