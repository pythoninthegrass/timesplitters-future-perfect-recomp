---
id: TASK-004
title: 'STATUS.md size: split by date/milestone or move measurements out'
status: To Do
assignee: []
created_date: '2026-11-06 04:29'
updated_date: '2026-11-06 04:30'
labels:
  - other
  - docs
  - maintenance
dependencies: []
references:
  - docs/project/STATUS.md
priority: low
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Deferred (from TASK-003). docs/project/STATUS.md has grown to ~40,400 lines / 3 MB as a newest-first validation log (931 '## ' headings, mostly '## YYYY-MM-DD - title'). It is too large to read whole. Plan, not done in TASK-003: split by month or release milestone, or move raw measurements/receipts to dated archive files (e.g. docs/project/status/2026-11.md) and keep a short index in STATUS.md. Preserve AGENTS.md/CI expectations for recording measured results while shrinking the hot file. Decide whether the retired MAC_PORT_BACKLOG integrity check leaves any STATUS.md cross-links to repoint.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A written split/archive plan exists with a proposed directory layout and index
- [ ] #2 Any STATUS.md existence/integrity expectations in tests and guides are identified
- [ ] #3 No historical validation evidence is lost by the chosen layout
<!-- AC:END -->
