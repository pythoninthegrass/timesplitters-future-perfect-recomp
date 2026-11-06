---
id: TASK-003.16
title: 'Mac validation: Story / System Link / Online multiplayer'
status: To Do
assignee: []
created_date: '2026-11-06 04:29'
updated_date: '2026-11-06 04:30'
labels:
  - feature
  - macos
  - mac-port
  - validation
dependencies: []
references:
  - docs/project/MAC_PORT_QUEUE.tsv
parent_task_id: TASK-003
priority: medium
ordinal: 2500
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Grouped validation task for the 1 Awaiting validation entries sharing this test path: tests/network/, tests/repository/test_story_coop_local.py, story evidence.

Run the shared checks and record per-entry Mac acceptance evidence for each MAC ID. Original per-feature detail (PC source, acceptance checks, evidence) is in the git history of docs/project/MAC_PORT_BACKLOG.md.

MAC IDs (1):
  - MAC-013: System Link and Online multiplayer
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every listed MAC ID has a recorded Mac acceptance result on tests/network/, tests/repository/test_story_coop_local.py, story evidence
- [ ] #2 Implementation vs. host/visual validation kept distinct per AGENTS.md
<!-- AC:END -->
