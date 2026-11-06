---
id: TASK-003.12
title: GPU / rendering & display
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
Grouped validation task for the 23 Awaiting validation entries sharing this test path: native Mac runner + tests/graphics/, render matrix cache.

Run the shared checks and record per-entry Mac acceptance evidence for each MAC ID. Original per-feature detail (PC source, acceptance checks, evidence) is in the git history of docs/project/MAC_PORT_BACKLOG.md.

MAC IDs (23):
  - MAC-010: In-game resolution preview and rollback
  - MAC-019: Framebuffer refresh between effects (issue #9)
  - MAC-020: Adaptive cutscene letterboxing (issue #33)
  - MAC-022: Configurable gameplay FOV (issue #29)
  - MAC-024: Resolution catalog and proportional UI (issues #27/#31)
  - MAC-027: Arcade RANK widget left placement
  - MAC-028: Preserve frontend camera FOV (#82)
  - MAC-032: Responsive menu backgrounds and scope masks
  - MAC-033: Full-display transition fades
  - MAC-035: Cinematic width fill (issue #30 investigation)
  - MAC-045: Terminal camera depth clears (issue #47)
  - MAC-047: Main-menu image and lettering fidelity
  - MAC-049: Spirit skull and eye rendering (#17)
  - MAC-054: Fractional presentation targets and Windows transform setup (issue #167)
  - MAC-056: Texture-camera composition alignment (issue #49)
  - MAC-058: Crane and remote-view vignette sizing (issue #221)
  - MAC-060: Native fractional updates at 60/120/144 FPS
  - MAC-063: Projected enemy health bars (issue #102)
  - MAC-082: Projected enemy shield effects (issue #358)
  - MAC-085: Shared impact spark timing (issue #371)
  - MAC-122: Temporary material matrix cache epoch (#398)
  - MAC-125: Assault objective widescreen placement (#338)
  - MAC-129: Optional SMAA anti-aliasing
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every listed MAC ID has a recorded Mac acceptance result on native Mac runner + tests/graphics/, render matrix cache
- [ ] #2 Implementation vs. host/visual validation kept distinct per AGENTS.md
<!-- AC:END -->
