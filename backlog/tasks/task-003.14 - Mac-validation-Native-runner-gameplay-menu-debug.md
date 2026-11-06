---
id: TASK-003.14
title: 'Mac validation: Native runner gameplay, menu & debug'
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
Grouped validation task for the 8 Awaiting validation entries sharing this test path: tools/testing/test-native-mac.py, tests/gameplay/, Test Lab fixture.

Run the shared checks and record per-entry Mac acceptance evidence for each MAC ID. Original per-feature detail (PC source, acceptance checks, evidence) is in the git history of docs/project/MAC_PORT_BACKLOG.md.

MAC IDs (8):
  - MAC-003: Debug settings and on-screen performance information
  - MAC-011: Real texture-pack gameplay coverage
  - MAC-023: Story Objectives health/shield (issue #11)
  - MAC-025: Reusable unlocked testing profile
  - MAC-026: Character picker and weapon proportions (issue #22)
  - MAC-029: Skippable idle demo video (#50)
  - MAC-031: Quit to Desktop menu entries
  - MAC-048: Companion vehicle zero-flag joins (#100)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every listed MAC ID has a recorded Mac acceptance result on tools/testing/test-native-mac.py, tests/gameplay/, Test Lab fixture
- [ ] #2 Implementation vs. host/visual validation kept distinct per AGENTS.md
<!-- AC:END -->
