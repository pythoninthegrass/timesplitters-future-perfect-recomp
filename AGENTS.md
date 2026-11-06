# Repository instructions

## Find the authoritative code

- Read `docs/agent-context/README.md`, then one relevant subsystem guide. Use
  `python tools/repo-context.py find <symbol-or-path>` before broad patch searches.
  The LOCAL SMART/Sol workflow in those guides is optional; it does not require
  OpenCode sessions to switch models or become advisory-only.
- Implement shared Windows/macOS/Linux behavior once in `src/` or reproducible
  `patches/`; keep OS and graphics-API operations in thin host adapters. `pc_`
  does not mean Windows-only. See `docs/development/shared-platform.md`.
- `vendor/ts3FPrecomp/source` is a byte-verified pristine snapshot, not an editing
  target. `external/ts3FPrecomp` is its ignored, patched working checkout and may
  contain valuable local edits. Prepare it offline with
  `python tools/build/prepare-runtime.py`; do not clone or reset it.
- Never edit generated guest C:
  `external/ts3FPrecomp/titles/futureperfect/src/recomp/gen/` (not `build/*/generated`).
  Change tracked source/generator/patches and regenerate instead.
- Apply the complete stack with
  `python tools/build/apply-patches.py external/ts3FPrecomp patches`.
  Effective order includes dependency overrides, not just numeric sorting.
  `patches/legacy/` is unwind-only; historical presentation patches remain required
  even though their feature was retired. Follow `patches/README.md` for additions.

## Build and focused checks

Run from the repository root. Use `.venv/bin/python` on Mac or
`.venv/Scripts/python.exe` on Windows in place of `python` below.

- Runtime/XBE pins live in `tsfp.ps1`; Python dependencies in `requirements.txt`,
  SDK pins in `config/build/`. Builders verify the supported US
  `private/game/default.xbe`; do not substitute another region/revision.
- Windows setup: `setup.ps1 -Python <python.exe> -Iso <game.iso>` runs Setup →
  Extract → Test → Generate → Build. Incremental build:
  `powershell -NoProfile -File tsfp.ps1 -Action Build`.
  Missing generated sources require `tsfp.ps1 -Action Generate` first.
  Output: `build/windows/Release/futureperfect_recomp.exe`.
- Apple Silicon: `python tools/build/build-native-mac.py --setup --generate --test`
  for initial setup/build; omit `--setup` thereafter, and use `--generate` when
  generator/hooks change. Output: `build/macos/futureperfect_recomp`.
  Auto selects Vulkan on macOS 26+, legacy GL otherwise; `--renderer gl` is an
  explicit fallback, not recovery from a failed SDK verification.
- Linux build/WSL prerequisites: `docs/development/linux.md`. Use `build/linux`
  and a Linux-local environment/checkout; never mutate one runtime concurrently
  from Windows and WSL.
- Focused test: `python -m pytest tests/<group>/test_<name>.py -q`;
  add `::test_name` or `-k <expression>` to narrow it. Prepare/apply runtime patches
  before tests extracting runtime bodies. Some original-code cases skip without
  the private XBE; skips do not establish coverage. Patch-transition suites are
  expensive; select checks using `docs/agent-context/build-test.md`.
- CI explicitly enumerates suites in `.github/workflows/runtime-patches.yml`;
  register new behavioral tests there. Launcher compatibility:
  `python tools/ci/launcher-compatibility.py --local`.
- For covered changes, update the owning guide(s) in
  `docs/agent-context/manifest.json` in the same change. After staging intended
  new patches, run `python tools/repo-context.py refresh` (index uses Git-indexed
  patch paths), then `python tools/repo-context.py check --base <task-base-revision>`.
  Focused maintenance test: `python -m pytest tests/repository/test_repo_context.py -q`.
  Documentation-only edits need no game rebuild.
- Preserve `.gitattributes`: patches/Python/Mac launchers use LF, `.ps1`/`.cmd`
  use CRLF; the binary watermark patch and pristine vendor files are exceptions.

## Validation and private data

- Never automate through interactive launchers or personal saves/settings.
  Windows: `python tools/testing/testing_profile.py --play --seconds 120`.
  Mac: `python tools/testing/test-native-mac.py --unlocked-profile --seconds 120`.
  These use disposable Test Lab copies; omit `--unlocked-profile` on Mac for
  fresh-profile tests. Preserve `private/test-fixtures/unlocked` unchanged.
- Isolate save/input paths and **both** `RECOMP_DISPLAY_CONFIG` and
  `TSFP_DISPLAY_CONFIG`. Preserve `private/saves`, `private/native-settings`,
  `config/pc-controls.json`, and `config/pc-display.ini`; create defaults only
  when absent. Storage changes must preserve existing saves on NTFS/exFAT and
  after relocation; sparse-file support is optional.
- Record measured checks and unrun host checks in `docs/project/STATUS.md`, with
  Mac adaptation/acceptance gaps in the matching Mac port Backlog task under
  `backlog/tasks/`. Build,
  startup, rendered menus, gameplay and physical-device validation are separate
  evidence. Keep original 60 FPS/60 Hz defaults; native high-FPS is opt-in, not
  the retired interpolation engine or permission to raise the interrupt clock.
- Keep the checkout lean: one `private/game` extract; no duplicate staging trees
  unless needed. Inspect `build/` before cleanup: it can contain Git worktrees.
  Use runner cleanup for disposable partition images, never broad `private/` cleanup.
- Textures are optional (`config/textures/texture-pack.json`); ordinary builds
  need no LFS hydration despite older build-guide wording. Preserve installed
  packs across updates. Texture publication requires hydrated DDS audits; keep
  the 6 GiB pack cap and private source artwork/recovery copies.

## Collaboration and release rules

- Use focused task branches, not permanent platform branches; do not merge into
  `main` without explicit instruction. After confirmed remote merge, safely remove
  only that task's local branch after checking for unique/uncommitted work.
- PR opening text uses only `## Change` and `## Cause and fix`, in user-facing
  language; technical validation belongs in the project records above.
- Keep fixed issues open until the containing version is published. Use
  `Refs #123`, not automatic-closing references, until then; verify and link the
  release before closing. This overrides older `Closes` advice in CONTRIBUTING.
- Game files, generated game code, personal settings/saves and private artwork
  stay local/ignored. Share source and patches through Git, not cross-OS virtual
  environments or build trees. For substantial investigations, keep a short
  ignored `logs/agent-investigation.md` with evidence, rejected hypotheses and
  the next check, rather than adding task history to this file.
