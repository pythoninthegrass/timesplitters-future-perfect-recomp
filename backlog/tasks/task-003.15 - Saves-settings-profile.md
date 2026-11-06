---
id: TASK-003.15
title: 'Saves, settings & profile'
status: To Do
assignee: []
created_date: '2026-11-06 04:29'
updated_date: '2026-11-06 05:11'
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
Grouped validation task for the 3 Awaiting validation entries sharing this test path: native-settings persistence, save-drive/storage relocation, profiles.

Run the shared checks and record per-entry Mac acceptance evidence for each MAC ID. Original per-feature detail (PC source, acceptance checks, evidence) is in the git history of docs/project/MAC_PORT_BACKLOG.md.

MAC IDs (3):
  - MAC-061: Host save-drive metadata and inline drive selection
  - MAC-119: Profile-scoped Unlock Content
  - MAC-124: Choose save folders (discussion 401)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every listed MAC ID has a recorded Mac acceptance result on native-settings persistence, save-drive/storage relocation, profiles
- [ ] #2 Implementation vs. host/visual validation kept distinct per AGENTS.md
<!-- AC:END -->
