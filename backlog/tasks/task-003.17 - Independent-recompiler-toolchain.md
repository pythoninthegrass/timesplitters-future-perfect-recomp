---
id: TASK-003.17
title: Independent recompiler toolchain
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
Grouped validation task for the 54 Awaiting validation entries sharing this test path: tests/compiler/, tools/compiler/, source generation + patch CI.

Run the shared checks and record per-entry Mac acceptance evidence for each MAC ID. Original per-feature detail (PC source, acceptance checks, evidence) is in the git history of docs/project/MAC_PORT_BACKLOG.md.

MAC IDs (54):
  - MAC-064: Self-contained runtime source
  - MAC-065: Independent game-disc import
  - MAC-066: Independent executable analysis
  - MAC-067: Independent disassembler input
  - MAC-068: Independent instruction traversal
  - MAC-069: Independent table and body recovery
  - MAC-070: Independent function discovery and metadata
  - MAC-071: Independent analysis runner and publication
  - MAC-072: Independent symbol adapter and pipeline driver
  - MAC-073: Independent function catalog
  - MAC-074: Independent generation support
  - MAC-075: Independent translator decoding
  - MAC-076: Independent translation layout and hook planning
  - MAC-077: Independent branch feedback and unresolved diagnostics
  - MAC-078: Independent C operand emission
  - MAC-079: Independent data-transfer and stack lowering
  - MAC-080: Independent scalar integer lowering
  - MAC-081: Independent shift and rotate lowering
  - MAC-083: Independent bit tests, scans and byte swaps
  - MAC-084: Independent multiply and divide lowering
  - MAC-086: Independent exchange lowering and atomic helpers
  - MAC-087: Independent comparison snapshots and sign extension
  - MAC-088: Independent string-instruction lowering
  - MAC-089: Independent condition-code generation
  - MAC-090: Independent SSE emission
  - MAC-091: Independent MMX emission
  - MAC-092: Independent x87 emission
  - MAC-093: Independent control-transfer emission
  - MAC-094: Independent instruction and block lifting
  - MAC-095: Independent lifter context and helper recognition
  - MAC-096: Independent batch translation and dispatch output
  - MAC-097: Independent translator context and entry discovery
  - MAC-098: Independent complete function emission
  - MAC-099: Independent translation command line
  - MAC-100: Project guest register and memory primitives
  - MAC-101: Project indirect guest-call dispatch
  - MAC-102: Project call checks and HLE argument frames
  - MAC-103: Project vector constructor and obsolete SIMD helper retirement
  - MAC-104: Direct scalar extension and numeric helper retirement
  - MAC-105: Canonical project guest execution header
  - MAC-106: Project branch-feedback provider and generated header
  - MAC-107: Project native continuation service
  - MAC-108: Project guest state and ABI diagnostics
  - MAC-109: Project native image loading
  - MAC-110: Project guest allocation ownership
  - MAC-111: Project guest thread storage
  - MAC-112: Project virtual-memory services
  - MAC-113: Project native memory ownership
  - MAC-114: Project guest memory services
  - MAC-115: Project native virtual-memory host operations
  - MAC-116: Project guest host mappings
  - MAC-117: Retired compatibility memory APIs
  - MAC-118: Independent kernel object lifetime
  - MAC-123: Bounded guest-memory crash evidence and model history
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every listed MAC ID has a recorded Mac acceptance result on tests/compiler/, tools/compiler/, source generation + patch CI
- [ ] #2 Implementation vs. host/visual validation kept distinct per AGENTS.md
<!-- AC:END -->
