---
id: TASK-003
title: Convert MAC_PORT_BACKLOG.md into ranked backlog tasks
status: Done
assignee:
  - Assistant
created_date: '2026-11-06 04:07'
updated_date: '2026-11-06 05:11'
labels:
  - docs
  - macos
  - backlog-migration
dependencies: []
references:
  - docs/project/MAC_PORT_QUEUE.tsv
  - docs/project/STATUS.md
  - tools/mac_backlog_queue.py
priority: medium
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
docs/project/MAC_PORT_BACKLOG.md was about 9,900 lines (700 KB) and docs/project/STATUS.md is about 40,000 lines (3 MB), too large to read in full by people or agents. The open Mac port work is now ranked Backlog tasks by type (bugs first, then features, CI, and other). Neither file was read whole: the queue table (## Queue) plus each '### MAC-nnn' heading gave ID, feature and status, captured by tools/mac_backlog_queue.py. Counts by status: 110 Awaiting validation, 7 Queued, 4 Verified, 3 In progress, 3 Not applicable, plus MAC-124/125 which had headings but no queue table row. Only Queued, In progress and Awaiting validation are actionable. Most open work is validation, not implementation, so validation tasks are grouped by shared test path instead of one task per MAC ID. Per the user's decision (2026-11-05) the ranked Backlog tasks are now authoritative: MAC_PORT_BACKLOG.md and tests/repository/test_mac_backlog.py were removed, docs/project/MAC_PORT_QUEUE.tsv preserves the queue data, and AGENTS.md points deferred adapter/acceptance work at backlog/tasks/.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Per-ID extraction script committed (tools/mac_backlog_queue.py) that lists ID, title and status from the queue table without reading the whole file
- [x] #2 Every Queued and In progress entry has a backlog task labeled bug, feature, ci or other, with its MAC ID reachable through a mac-nnn label, the description and the queue snapshot; titles stay plain because labels already carry the classification (user instruction, 2026-11-05)
- [x] #3 Awaiting validation entries grouped into validation tasks by shared test path (native Mac runner, launcher tests, GPU contracts, and so on), each listing its MAC IDs
- [x] #4 Tasks ordered bugs, then features, then CI, then other, using backlog priority
- [x] #5 Decision recorded (user, 2026-11-05): the ranked Backlog tasks are authoritative; MAC_PORT_BACKLOG.md and the CI ID/status integrity check were removed and AGENTS.md plus the docs now point at backlog/tasks/
- [x] #6 Plan for STATUS.md size (split by date or milestone, or move measurements elsewhere) written up as follow-up TASK-005, not done here
<!-- AC:END -->





## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Approved 2026-11-05 (user). Decision (AC#5): the ranked Backlog tasks become authoritative; docs/project/MAC_PORT_BACKLOG.md is deleted after capture; tests/repository/test_mac_backlog.py is removed (CI is being gutted separately, so guide/CI edits kept minimal); STATUS.md work deferred to TASK-005. Work isolated in worktree branch chore/mac-backlog-migration (main checkout is shared with other agents).
Steps:
1. tools/mac_backlog_queue.py (AC#1): parses only the '## Queue' table region, folds in the MAC-124/125 headings missing from the table, derives issue #, assigns type (bug/feature/ci/other) + validation group; --check enforces that every actionable entry is classified exactly once. Generates docs/project/MAC_PORT_QUEUE.tsv (127-row snapshot preserving ID/title/status).
2. Tasks (AC#2-4): 19 children of TASK-003 = 10 individual (every Queued+In progress; bugs first) + 9 validation groups grouped by shared test path; TASK-005 STATUS.md follow-up is top-level. Ordered by priority+ordinal: bugs(high,1000s) > features(medium,2000s) > ci(medium,3000s) > other(low,4000s).
3. Delete docs/project/MAC_PORT_BACKLOG.md + tests/repository/test_mac_backlog.py; drop the test from .github/workflows/runtime-patches.yml.
4. Full scrub of MAC_PORT_BACKLOG references (README/CONTRIBUTING/docs/players+development/agents guides/tools); update owning guides build-test.md + investigation.md; run repo-context check --base.
Do not push or merge to main without explicit instruction.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Committed as 20075983 on branch chore/mac-backlog-migration (not pushed, not merged into main). docs/project/MAC_PORT_BACKLOG.md and tests/repository/test_mac_backlog.py removed; docs/project/MAC_PORT_QUEUE.tsv (127 rows) and tools/mac_backlog_queue.py added; 19 children under TASK-003 (10 individual Queued/In progress, 9 grouped validation tasks covering the 110 Awaiting validation entries) plus top-level TASK-005 for the deferred STATUS.md size work. AGENTS.md, README, CONTRIBUTING and eight docs now point at backlog/tasks/. Verified: repo-context check --base main passes; tests/repository + tests/launcher give 656 passed, with 22 errors and 1 failure that are pre-existing environment gaps in this fresh worktree (missing ignored external/ts3FPrecomp checkout, and pytest-xdist absent for the -n option). Known gap left open: docs/project/STATUS.md still has about 30 internal links to the deleted file, deferred with its size work to TASK-005. MAC-124 and MAC-125 had headings but no queue table row, a pre-existing gap the retired integrity check never saw because it parsed only three-hash headings.
<!-- SECTION:FINAL_SUMMARY:END -->
