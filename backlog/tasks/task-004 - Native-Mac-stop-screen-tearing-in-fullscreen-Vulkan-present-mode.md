---
id: TASK-004
title: 'Native Mac: stop screen tearing in fullscreen (Vulkan present mode)'
status: To Do
assignee: []
created_date: '2026-11-06 04:29'
labels:
  - bug
  - macos
  - graphics
dependencies: []
references:
  - vendor/ts3FPrecomp/source/src/d3d/rhi_vulkan.c
priority: high
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fullscreen 1080p on native Mac (MoltenVK, Apple M4) tears. Launcher log shows 'present mode IMMEDIATE' (logs/native-play.err) and 'presentation interval 0x00000001 -> 0x00000000': the runtime rewrites the title's vsync request to interval 0, and choose_mode() in rhi_vulkan.c then falls to IMMEDIATE because MoltenVK offers no MAILBOX. RECOMP_VK_PRESENT=fifo would select FIFO, but the launcher does not forward that variable to Bin/futureperfect_recomp, and no runtime.conf key or launcher row controls the present mode. FIFO must not be the default for interval 0: the choose_mode comment records a Burnout 2 loader regression (136 to 27 fps) from a blocking present. Scope the fix to gameplay presentation, keep 60 FPS (Original) behaviour, and implement once in shared source or the shared patch stack, not as a Mac-only copy.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Failing test written first for the present-mode choice (interval 1, interval 0, vrr, available-mode sets with and without MAILBOX) and confirmed to fail before the fix
- [ ] #2 A user-visible setting (runtime.conf key plus launcher row, shared Windows/Mac model) selects vsync/FIFO versus the current non-blocking order; unsupported saved values are preserved
- [ ] #3 Setting reaches the game process from the launcher; the log's '[RHI] ... present mode' line shows the selected mode
- [ ] #4 Loader and movie paths that need non-blocking present are not throttled when vsync is on (check the interval-0 callers, cf. Burnout 2 note in choose_mode)
- [ ] #5 Behaviour with frame_cap 60, 120/144 FPS beta, and vrr=1 is stated and tested; no change to the console interrupt clock
- [ ] #6 Change is a separate patch in the shared stack, owning agent-context guide updated, and this task records the PC behaviour, files, Mac status and acceptance checks
- [ ] #7 Mac validation recorded in docs/project/STATUS.md with host, macOS version, MoltenVK version and a before/after capture; Windows/Linux paths reviewed for regressions
<!-- AC:END -->
