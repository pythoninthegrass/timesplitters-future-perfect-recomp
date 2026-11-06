---
id: TASK-001
title: Reduce clone size by skipping LFS texture download by default
status: Done
assignee:
  - Assistant
created_date: '2026-11-06 04:01'
updated_date: '2026-11-06 04:28'
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
- [x] #1 Source-only clone path documented (GIT_LFS_SKIP_SMUDGE=1 git clone, or git lfs install --skip-smudge) with the git lfs pull step for texture work
- [x] #2 CI workflows checked to confirm LFS is only fetched by jobs that need it (unverified in the issue)
- [x] #3 Decision recorded on publishing compiled textures as release assets instead of LFS tracking
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Approved plan (2026-11-06, user chose CI hardening + docs-only decision home, no public posting).

Measured findings (this checkout, main @5ff1e114):
- du: . 3.1G, assets/ 1.5G, .git/lfs 1.5G, .git/objects 34M -> matches issue #501.
- Only assets/textures/*.dds is LFS-tracked (.gitattributes); git lfs ls-files = 6,812.
- Packets are optional: config/textures/texture-pack.json delivery="optional"; tsfp.ps1:155 only runs tools/textures/build_textures.py when delivery=="bundled"; build_textures.py:43/48 raise the "run git lfs pull" errors only when a pack is really required. So a pointer-only checkout builds.
- Player delivery is ALREADY release assets: tools/textures/texture-release.py publishes textures-v<version> with bounded hashed parts; launcher reads config/texture-download.json from raw.githubusercontent (tools/launcher/TextureDownload.cs:51).
- CI: of 12 workflows only .github/workflows/texture-pack.yml sets lfs: true; all other actions/checkout steps omit it (default false -> pointers). No workflow runs git lfs pull/checkout/reset after checkout. texture-pack.yml is gated by tools/ci/ci-runtime-scope.py 'textures' patterns.
- Stale doc to fix: docs/development/building.md:30 tells contributors to run git lfs install && git lfs pull after cloning.

Steps:
1. Isolate: worktree branch task-001-lfs-clone-size (main checkout has another agent's uncommitted AGENTS.md rewrite; AGENTS.md and docs/agent-context/investigation.md are off-limits to me). Backlog record stays in the main checkout.
2. AC#1 docs: rewrite building.md clone paragraph; add "Source-only checkout" subsection to docs/textures/textures.md (GIT_LFS_SKIP_SMUDGE=1 git clone, git lfs install --skip-smudge, git lfs pull for asset work, how to tell a pointer from DDS bytes); contributor pointer in README.md/CONTRIBUTING.md; note in docs/development/repository-layout.md; mirror Mac/Linux guides only if they carry clone steps.
3. AC#2 CI: add explicit lfs: false to every non-texture actions/checkout step (immune to upstream default changes); record the per-workflow audit table in docs/agent-context/runtime-ci.md and docs/project/STATUS.md; prove it by running the CI texture verification and release-profile texture suites in a fresh pointer-only clone in the temp dir, and by grepping recent Actions logs for LFS "Filtering content" outside the texture job. No new behavioral test (user choice).
4. AC#3: "Texture storage and distribution decision" section in docs/textures/textures.md - LFS stays the authoring/build-input store, player delivery stays hashed GitHub Release assets; trade-offs and revisit triggers. Mirrored as a STATUS.md evidence line.
5. Guides/checks: update owning guides per docs/agent-context/manifest.json (systems.md for assets/textures, build-test.md for build/CI claims); run tools/repo-context.py refresh then check --base main; focused suites tests/repository/test_repo_context.py, tests/textures/test_build_textures.py, tests/textures/test_texture_release.py, tests/repository/test_ci_runtime_scope.py.
6. Close-out: check acceptance criteria, log notes/evidence, PR text limited to "## Change" and "## Cause and fix", Refs #501 (not Closes), no merge to main without instruction.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Branch/worktree: task/001-lfs-clone-size (commit 8bd175d9) at /Users/lance/.local/share/opencode/worktree/bafad0/task-001-lfs-clone-size. Main checkout left untouched because another agent has an uncommitted AGENTS.md rewrite; AGENTS.md and docs/agent-context/investigation.md were off-limits.

User decisions: CI hardening (explicit lfs: false) rather than audit-only or audit+test; no public posting on issue #501; decision recorded in docs/textures/textures.md rather than a new decision doc.

docs/agent-context/build-test.md sits exactly at the 65,536-byte context cap (tools/repo-context.py safe_file), so guide edits must be byte-neutral or smaller. Freed bytes by deleting 'Native Windows45m/Mac30m; upgrades30m.', already documented in runtime-ci.md, whose overview link at build-test.md:529 already delegates job budgets.

No repository .venv existed on this Mac; created .venv in the worktree with uv from requirements.txt pins (pytest 9.1.1 etc.) for the focused suites.

Issue #501's '~70 MB' source-only estimate is optimistic for a different reason than content size. Re-measured 2026-11-05 in one `GIT_LFS_SKIP_SMUDGE=1 git clone --no-local`: 126 MB total = 34 MB `.git` (no LFS objects) + about 92 MB working tree, of which only 35 MB is content; the rest is 4 KiB block overhead across 16,433 files. `assets/` alone is 53 MB because the 6,812 pointers (1.5 MiB of data) and 6,812 metadata JSON files (1.5 MiB) each take a block. An earlier note here recorded '129 MB (53 MB working tree, 37 MB .git)'; 53 MB is `assets/` alone and 37 MB was a worktree `.git`, so that split came from two different checkouts and is superseded.

Texture pack budget is 6 GiB (tools/textures/texture-release.py BUDGET = 6*1024**3, error text '6 GiB / 20,000 texture limits'), and AGENTS.md:86 matches it ('keep the 6 GiB pack cap'). An earlier note here claimed the other agent's uncommitted AGENTS.md rewrite said '6 MiB pack cap'; re-checked 2026-11-05, no tracked file contains '6 MiB' as a pack cap. That claim was my misreading and is withdrawn.

Pre-existing local failures, identical in hydrated and pointer-only clones (5 failed, 29 passed, 2 skipped, 22 errors in the four native texture suites): they need the prepared external/ts3FPrecomp runtime, which a fresh worktree lacks. Not LFS-related and not counted as coverage.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Change

A fresh clone now has a documented source-only path, and CI states its LFS intent on every checkout.

- **Clone documentation** (AC#1). New "Clone the source" section in `docs/development/building.md` gives both `GIT_LFS_SKIP_SMUDGE=1 git clone` forms (PowerShell and POSIX) and `git lfs install --local|--global --skip-smudge`, the `git lfs pull` step for asset work, how to tell a pointer (130-byte text, `version https://git-lfs.github.com/spec/v1`) from DDS bytes (`DDS `), and the measured sizes: 126 MB pointer-only versus 3.1 GB hydrated. `docs/textures/textures.md` gained a "Source-only checkout" subsection, and README/CONTRIBUTING/repository-layout/Linux guide now point at the path instead of assuming a 3 GB clone. The stale Windows text that told contributors to run `git lfs install`/`git lfs pull` after cloning, and claimed an LFS checkout was "the supported build input", is replaced with the real rule: `tsfp.ps1` audits `assets/textures` only when `config/textures/texture-pack.json` declares `bundled` delivery.
- **CI audit** (AC#2). All 12 workflows / 22 checkout steps were examined. Only `.github/workflows/texture-pack.yml` requested LFS, gated by `tools/ci/ci-runtime-scope.py` "textures" patterns, and no job ran `git lfs pull`/`git checkout` afterwards. The other 21 checkout steps now state `lfs: false` explicitly so an upstream default change cannot hydrate 1.5 GiB in an unrelated job; the texture job keeps `lfs: true`. Audit results and reproduction commands are recorded in `docs/agent-context/runtime-ci.md` and `docs/project/STATUS.md`.
- **Storage decision** (AC#3). New "Storage decision: LFS and release assets" section in `docs/textures/textures.md`: player distribution already uses hashed GitHub release assets (`tools/textures/texture-release.py` publishes `textures-v<version>`; the launcher reads `config/texture-download.json`), so the stable-URL/no-retention goal is met, while LFS stays the authoritative authoring/build input that travels with the source revision. Trade-offs and three revisit triggers are recorded.
- **Guides**: owning guides updated per `docs/agent-context/manifest.json` (build-test.md for `runtime-patches.yml`, launcher.md for the issue/launcher workflows, plus runtime-ci.md).

## Cause and fix

The repository's only Git LFS content is 6,812 optional compiled DDS files. Git LFS hydrates them on every clone by default, so contributors paid about 3 GB (1.5 GiB working tree plus 1.5 GiB `.git/lfs`) for artwork that ordinary builds and packages never read. Documentation also still described the retired always-hydrated build. This makes the cheap clone the documented default, keeps hydration an explicit per-checkout action, and pins the CI policy in the workflow files themselves.

## Validation

- `GIT_LFS_SKIP_SMUDGE=1` clone of this revision (`git clone --no-local`): 126 MB total — 34 MB `.git` with no LFS objects, about 92 MB working tree (35 MB content, rest 4 KiB block overhead over 16,433 files; `assets/` alone 53 MB) — with all DDS as pointers (`git lfs ls-files -s` shows no hydrated entries). The hydrated checkout measures 3.1 GB, with 6,812 DDS files at 1,572,457,676 bytes on disk and 1,574,002,482 `installed_bytes` advertised by the download index.
- In that pointer-only clone the Repository texture pack verification fails with "Texture files are Git LFS pointers. Run git lfs pull before building or packaging." (proving that job needs `lfs: true`), while `tests/textures/test_build_textures.py` and `test_texture_release.py` pass unchanged (19 passed, 3 subtests). The four native texture suites produced identical results hydrated versus pointer-only (5 failed, 29 passed, 2 skipped, 22 errors); the failures need the unprepared `external/ts3FPrecomp` runtime, so they are an environment gap, not LFS evidence.
- actionlint 1.7.12 clean on all 12 workflows; every YAML still parses with the expected `lfs` values.
- Focused suites: `test_repo_context.py`, `test_ci_runtime_scope.py`, `test_build_textures.py`, `test_texture_release.py`, `test_launcher_release.py` = 164 passed plus 13 subtests; `test_ci_pr_gate.py`, `test_launcher_compatibility.py` = 67 passed plus 31 subtests. `tools/repo-context.py refresh` then `check --base 5ff1e114` passed.

## Risks and follow-ups

- Work lived on branch `task/001-lfs-clone-size` (commit 8bd175d9) in an OpenCode worktree; on instruction it was fast-forward merged into local `main` and the worktree removed. Not pushed, and the issue #501 comment was deliberately not posted.
- Follow-up committed 2026-11-05: the clone-size figures in `docs/development/building.md`, `docs/textures/textures.md` and this task record were re-measured in a single checkout and corrected (see Implementation Notes).
- Not run: hosted Actions for these workflow edits, a Windows or Mac native build from a source-only clone, and game launch/validation of any kind.
- `docs/agent-context/build-test.md` sits exactly at the 65,536-byte context cap, so future guide edits there must be byte-neutral; the removed duplicate job-budget sentence already lives in `runtime-ci.md`.
- Corrected here after the fact: no AGENTS.md version says "6 MiB pack cap". Working-tree `AGENTS.md:86` says "keep the 6 GiB pack cap", which matches `tools/textures/texture-release.py` (`BUDGET = 6 * 1024**3`). The earlier "discrepancy" in this task record was an assistant misreading, not a repository defect.
<!-- SECTION:FINAL_SUMMARY:END -->
