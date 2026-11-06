---
id: TASK-002
title: 'macOS launcher: keep saves, settings and textures in Application Support'
status: To Do
assignee: []
created_date: '2026-11-06 04:01'
labels:
  - upstream-idea
  - macos
  - launcher
dependencies: []
references:
  - tools/launcher/macos/Program.cs
  - >-
    https://github.com/TheDoffman/timesplitters-future-perfect-pc/discussions/new?category=ideas
priority: medium
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The macOS launcher uses the folder containing TimeSplitters Launcher.app as its install root (FindRoot in tools/launcher/macos/Program.cs). Saves, Settings, Textures, Data, logs and the game build all live there, so installing under /Applications puts user data next to the app, and an alias does not help because the root follows the real bundle location. Proposed: default to ~/Library/Application Support/TimeSplitters for user data on macOS, keep portable-folder and --root behavior, and let users pick an existing data folder so moving does not lose saves. Interim workaround: move the whole install folder and start it with Launch.command, which passes --root. Intended as a post in the upstream Ideas discussions category (blank issues are disabled); not yet posted.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Data directory default on macOS is ~/Library/Application Support/TimeSplitters outside portable and checkout layouts
- [ ] #2 Existing portable installs and explicit --root keep working without moving data
- [ ] #3 Users can select an existing data folder; saves are never reset or overwritten on relocation
<!-- AC:END -->
