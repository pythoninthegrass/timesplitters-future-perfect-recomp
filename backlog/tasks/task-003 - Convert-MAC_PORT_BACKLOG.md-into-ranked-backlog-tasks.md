---
id: TASK-003
title: Convert MAC_PORT_BACKLOG.md into ranked backlog tasks
status: To Do
assignee: []
created_date: '2026-11-06 04:07'
labels:
  - docs
  - macos
  - backlog-migration
dependencies: []
references:
  - docs/project/MAC_PORT_BACKLOG.md
  - docs/project/STATUS.md
priority: medium
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
docs/project/MAC_PORT_BACKLOG.md is about 9,900 lines (700 KB) and docs/project/STATUS.md is about 40,000 lines (3 MB), too large to read in full by people or agents. Convert the open Mac port work into backlog tasks ranked by type (bugs first, then features, CI, and other). Do not read either file whole. The 125-row queue table (## Queue) gives ID, feature and status for every entry, and each entry has a '### MAC-nnn' heading, so use rg for headings, table rows and per-entry sections. Current counts by status: 108 Awaiting validation, 7 Queued, 4 Verified, 3 In progress, 3 Not applicable. Only Queued, In progress and Awaiting validation are actionable. Most open work is validation, not implementation, so group validation tasks by shared test path instead of one task per MAC ID. AGENTS.md requires backlog entries and CI checks ID/status integrity in this file, so it cannot simply be deleted.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Per-ID extraction script or rg recipe committed that lists ID, title and status from the queue table without reading the whole file
- [ ] #2 Every Queued and In progress entry has a backlog task, labeled bug, feature, ci or other, with the MAC ID and any issue number in the title or references
- [ ] #3 Awaiting validation entries grouped into validation tasks by shared test path (for example native Mac runner, launcher tests, GPU contracts), each listing its MAC IDs
- [ ] #4 Tasks ordered bugs, then features, then CI, then other, using backlog priority
- [ ] #5 Decision recorded on whether MAC_PORT_BACKLOG.md stays authoritative, and AGENTS.md and the CI ID/status integrity check updated to match
- [ ] #6 Plan for STATUS.md size (split by date or milestone, or move measurements elsewhere) written up as a follow-up task, not done here
<!-- AC:END -->
