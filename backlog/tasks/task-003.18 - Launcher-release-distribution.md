---
id: TASK-003.18
title: 'Launcher, release & distribution'
status: To Do
assignee: []
created_date: '2026-11-06 04:29'
updated_date: '2026-11-06 05:11'
labels:
  - ci
  - macos
  - mac-port
  - validation
dependencies: []
references:
  - docs/project/MAC_PORT_QUEUE.tsv
parent_task_id: TASK-003
priority: medium
ordinal: 3500
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Grouped validation task for the 7 Awaiting validation entries sharing this test path: tests/launcher/, packaging/version/provenance, release channels.

Run the shared checks and record per-entry Mac acceptance evidence for each MAC ID. Original per-feature detail (PC source, acceptance checks, evidence) is in the git history of docs/project/MAC_PORT_BACKLOG.md.

MAC IDs (7):
  - MAC-015: Release test privileges and disposable cleanup
  - MAC-021: Published-release launcher and pre-game settings
  - MAC-044: Game crash capture and launcher reports
  - MAC-051: Version and build-identity watermark
  - MAC-057: Optional texture pack delivery through the launcher
  - MAC-062: Stable and named game release channels
  - MAC-127: Complete launcher language packs
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every listed MAC ID has a recorded Mac acceptance result on tests/launcher/, packaging/version/provenance, release channels
- [ ] #2 Implementation vs. host/visual validation kept distinct per AGENTS.md
<!-- AC:END -->
