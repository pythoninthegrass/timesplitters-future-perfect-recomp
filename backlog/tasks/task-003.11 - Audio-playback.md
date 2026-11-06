---
id: TASK-003.11
title: Audio playback
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
Grouped validation task for the 2 Awaiting validation entries sharing this test path: native audio playback, story audio timing.

Run the shared checks and record per-entry Mac acceptance evidence for each MAC ID. Original per-feature detail (PC source, acceptance checks, evidence) is in the git history of docs/project/MAC_PORT_BACKLOG.md.

MAC IDs (2):
  - MAC-018: Story audio timing, queue retry and ADPCM resume (issue #8)
  - MAC-120: Enhanced Audio beta
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every listed MAC ID has a recorded Mac acceptance result on native audio playback, story audio timing
- [ ] #2 Implementation vs. host/visual validation kept distinct per AGENTS.md
<!-- AC:END -->
