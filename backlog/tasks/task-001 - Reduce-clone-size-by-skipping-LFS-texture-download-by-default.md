---
id: TASK-001
title: Reduce clone size by skipping LFS texture download by default
status: To Do
assignee: []
created_date: '2026-11-06 04:01'
labels:
  - upstream-issue
  - lfs
  - docs
dependencies: []
references:
  - 'https://github.com/TheDoffman/timesplitters-future-perfect-pc/issues/501'
priority: medium
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Upstream issue #501: a fresh clone is about 3 GB on disk because 6,812 LFS texture files under assets/textures (about 1.5 GiB) are downloaded by default and stored twice (working tree and .git/lfs). Everything else tracked is about 70 MB. AGENTS.md already says ordinary source builds and game packaging need no texture hydration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Source-only clone path documented (GIT_LFS_SKIP_SMUDGE=1 git clone, or git lfs install --skip-smudge) with the git lfs pull step for texture work
- [ ] #2 CI workflows checked to confirm LFS is only fetched by jobs that need it (unverified in the issue)
- [ ] #3 Decision recorded on publishing compiled textures as release assets instead of LFS tracking
<!-- AC:END -->
