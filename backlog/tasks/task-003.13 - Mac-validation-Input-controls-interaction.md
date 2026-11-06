---
id: TASK-003.13
title: 'Mac validation: Input, controls & interaction'
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
Grouped validation task for the 10 Awaiting validation entries sharing this test path: native runner physical input, tests/gameplay/ input, config/pc-controls.json.

Run the shared checks and record per-entry Mac acceptance evidence for each MAC ID. Original per-feature detail (PC source, acceptance checks, evidence) is in the git history of docs/project/MAC_PORT_BACKLOG.md.

MAC IDs (10):
  - MAC-001: Direct-camera mouse look
  - MAC-002: Keyboard/mouse prompts and device switching
  - MAC-004: Capture-to-bind and conflict reassignment
  - MAC-016: Shared pickup-range comparison fix (issue #6)
  - MAC-030: Menu mouse selection (#86)
  - MAC-043: Automatic mouse Auto Lookahead override
  - MAC-055: Persist accepted frontend Controls before quitting Settings
  - MAC-059: Physical keyboard entry in original text dialogs (issue #136)
  - MAC-121: High-FPS interaction input (#357)
  - MAC-128: Fresh weapon trigger timing (#434)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every listed MAC ID has a recorded Mac acceptance result on native runner physical input, tests/gameplay/ input, config/pc-controls.json
- [ ] #2 Implementation vs. host/visual validation kept distinct per AGENTS.md
<!-- AC:END -->
