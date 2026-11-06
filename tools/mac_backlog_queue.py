#!/usr/bin/env python3
"""Extract the Mac port queue without reading the whole handoff file.

The Mac port handoff (``docs/project/MAC_PORT_BACKLOG.md``) grew to thousands of
lines of per-feature prose that is too large for a person or an agent to read
whole.  Every actionable row already lives in the ``## Queue`` table as
``| ID | Feature | Status |`` and each feature has a ``### MAC-nnn`` heading, so
this tool reads only that bounded region plus the heading lines and reports a
ranked, classified view.

It is the reproducible provenance for the ranked Backlog tasks
(``backlog/tasks/``): it lists ID, title and status from the queue table, folds
in any ``## MAC-nnn`` heading that was missing from the table, derives the
GitHub issue number from the title, and assigns each actionable entry a type
(``bug``/``feature``/``ci``/``other``) and a validation ``group`` keyed to a
shared test path.  Verified / Not applicable rows are reported but not grouped.

Usage:
    python tools/mac_backlog_queue.py                 # markdown report to stdout
    python tools/mac_backlog_queue.py --format tsv    # TSV to stdout
    python tools/mac_backlog_queue.py --format json   # JSON to stdout
    python tools/mac_backlog_queue.py --write-snapshot docs/project/MAC_PORT_QUEUE.tsv
    python tools/mac_backlog_queue.py --check         # exit non-zero on gaps

The handoff file is deleted once the ranked tasks exist; ``--source`` still works
against a saved copy and the committed snapshot
(``docs/project/MAC_PORT_QUEUE.tsv``) preserves the queue data afterwards.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = "docs/project/MAC_PORT_BACKLOG.md"

ACTIONABLE = {"Queued", "In progress", "Awaiting validation"}
KNOWN_STATUSES = ACTIONABLE | {"Verified", "Not applicable"}

# Individual tasks: every Queued / In progress entry gets its own task.
# Queued: 009 036 040 041 042 046 052 | In progress: 005 006 007
INDIVIDUAL = {
    "MAC-036": "bug",      # Ghost Gun full-body visibility (issue #111)
    "MAC-046": "bug",      # Update transaction rename contention
    "MAC-005": "feature",  # Multiple texture stages and shader fidelity
    "MAC-006": "feature",  # Cube and volume texture resources
    "MAC-007": "feature",  # Screen-copy effects and image surfaces
    "MAC-009": "feature",  # Intro and in-game movie playback
    "MAC-041": "feature",  # Published game version picker and banner replacement
    "MAC-042": "feature",  # Formatted release notes and browser links
    "MAC-052": "feature",  # Experimental network bot setup (issue #25)
    "MAC-040": "other",    # Dedicated game icon
}

# Validation groups: every Awaiting validation entry belongs to exactly one,
# keyed to the shared test/validation route named in ``route``.  ``ids`` are
# the MAC numbers (zero-padded) assigned to the group.
GROUPS = {
    "GPU / rendering & display": {
        "type": "feature",
        "route": "native Mac runner + tests/graphics/, render matrix cache",
        "ids": ["010", "019", "020", "022", "024", "027", "028", "032", "033",
                "035", "045", "047", "049", "054", "056", "058", "060", "063",
                "082", "085", "122", "125", "129"],
    },
    "Input, controls & interaction": {
        "type": "feature",
        "route": "native runner physical input, tests/gameplay/ input, config/pc-controls.json",
        "ids": ["001", "002", "004", "016", "030", "043", "055", "059", "121", "128"],
    },
    "Native runner gameplay, menu & debug": {
        "type": "feature",
        "route": "tools/testing/test-native-mac.py, tests/gameplay/, Test Lab fixture",
        "ids": ["003", "011", "023", "025", "026", "029", "031", "048"],
    },
    "Story / System Link / Online multiplayer": {
        "type": "feature",
        "route": "tests/network/, tests/repository/test_story_coop_local.py, story evidence",
        "ids": ["013"],
    },
    "Saves, settings & profile": {
        "type": "feature",
        "route": "native-settings persistence, save-drive/storage relocation, profiles",
        "ids": ["061", "119", "124"],
    },
    "Audio playback": {
        "type": "feature",
        "route": "native audio playback, story audio timing",
        "ids": ["018", "120"],
    },
    "Independent recompiler toolchain": {
        "type": "ci",
        "route": "tests/compiler/, tools/compiler/, source generation + patch CI",
        "ids": [
            *[f"{n:03d}" for n in range(64, 100) if n not in (82, 85)],
            *[f"{n:03d}" for n in range(100, 119)],
            "123",
        ],
    },
    "Launcher, release & distribution": {
        "type": "ci",
        "route": "tests/launcher/, packaging/version/provenance, release channels",
        "ids": ["015", "021", "044", "051", "057", "062", "127"],
    },
    "Discord & community": {
        "type": "other",
        "route": "Discord Rich Presence and launcher community buttons",
        "ids": ["053", "126"],
    },
}

# Ordered type ranking used for the "bugs, then features, then CI, then other"
# requirement; lower sorts earlier.
TYPE_ORDER = {"bug": 0, "feature": 1, "ci": 2, "other": 3}

_ISSUE_RE = re.compile(r"#(\d+)")
_TABLE_ROW_RE = re.compile(r"^\|\s*(MAC-\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", re.M)
_HEADING_RE = re.compile(r"^#{2,3}\s+(MAC-\d+)\b[ \t]*[—-][ \t]*(.+?)[ \t]*$", re.M)


def _parse_queue(text: str) -> dict[str, tuple[str, str]]:
    """Return {id: (title, status)} from the ``## Queue`` table only."""
    if "## Queue\n" not in text:
        raise SystemExit("No '## Queue' table found")
    region = text.split("## Queue\n", 1)[1]
    # The per-feature sections begin at the first '### ' heading; stop there so
    # only the table is scanned (never the whole file body).
    region = region.split("\n### ", 1)[0]
    rows: dict[str, tuple[str, str]] = {}
    for match in _TABLE_ROW_RE.finditer(region):
        identifier, title, status = match.group(1), match.group(2), match.group(3)
        if identifier in rows:
            raise SystemExit(f"Duplicate queue ID in table: {identifier}")
        rows[identifier] = (title.strip(), status.strip())
    return rows


def _parse_headings(text: str) -> dict[str, tuple[str, str]]:
    """Return {id: (title, status)} from ``##/### MAC-nnn`` headings.

    The heading format is ``### MAC-nnn - Title`` or ``### MAC-nnn — Title``;
    a trailing `` - Status`` (used by hand-added two-hash entries) is recognised.
    """
    found: dict[str, tuple[str, str]] = {}
    for match in _HEADING_RE.finditer(text):
        identifier, rest = match.group(1), match.group(2).strip()
        status = ""
        tail = rest.rsplit(" - ", 1)
        if len(tail) == 2 and tail[1].strip() in KNOWN_STATUSES:
            rest, status = tail[0].strip(), tail[1].strip()
        found.setdefault(identifier, (rest, status))
    return found


def _issue(title: str) -> str:
    issues = _ISSUE_RE.findall(title)
    return "#".join(issues) if issues else ""


def _classify(identifier: str, status: str) -> tuple[str, str]:
    """Return (type, group) for an actionable entry; ('', '') when not actionable."""
    if status not in ACTIONABLE:
        return "", ""
    if identifier in INDIVIDUAL:
        return INDIVIDUAL[identifier], f"individual ({identifier})"
    if status == "Awaiting validation":
        number = identifier.split("-")[1]
        for group, spec in GROUPS.items():
            if number in spec["ids"]:
                return spec["type"], group
    return "", ""


def extract(source: Path) -> tuple[list[dict], list[str], list[str]]:
    """Return (entries, missing_from_groups, extra_in_groups)."""
    text = source.read_text(encoding="utf-8")
    table = _parse_queue(text)
    headings = _parse_headings(text)
    missing_rows: list[str] = []  # headings absent from the table

    merged: dict[str, tuple[str, str]] = dict(table)
    for identifier, (title, status) in headings.items():
        if identifier not in merged:
            missing_rows.append(identifier)
            merged[identifier] = (title, status or "Awaiting validation")

    entries = []
    for identifier, (title, status) in merged.items():
        type_, group = _classify(identifier, status)
        entries.append({
            "id": identifier,
            "number": int(identifier.split("-")[1]),
            "title": title,
            "status": status,
            "issue": _issue(title),
            "type": type_,
            "group": group,
            "in_table": identifier in table,
        })
    entries.sort(key=lambda e: (TYPE_ORDER.get(e["type"], 9), e["number"]))

    # Coverage self-check: every awaiting-validation entry must be in one group.
    actionable_ids = {e["id"] for e in entries if e["status"] in ACTIONABLE}
    awaiting_ids = {e["id"] for e in entries if e["status"] == "Awaiting validation"}
    grouped: set[str] = set()
    for spec in GROUPS.values():
        for number in spec["ids"]:
            grouped.add(f"MAC-{number}")
    missing_from_groups = sorted(awaiting_ids - grouped)
    extra_in_groups = sorted(grouped - actionable_ids)
    _ = actionable_ids
    return entries, missing_from_groups, extra_in_groups


def _fmt_markdown(entries: list[dict], missing_rows: list[str]) -> str:
    lines = ["| ID | Type | Group | Status | Issue | In table | Title |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for e in entries:
        lines.append(
            f"| {e['id']} | {e['type'] or '-'} | {e['group'] or '-'} | {e['status']} "
            f"| {e['issue'] or '-'} | {'yes' if e['in_table'] else 'NO'} | {e['title']} |"
        )
    if missing_rows:
        lines.append("")
        lines.append("Headings missing from the queue table: " + ", ".join(sorted(missing_rows)))
    return "\n".join(lines)


def _fmt_tsv(entries: list[dict]) -> str:
    header = "id\ttype\tgroup\tstatus\tissue\tin_table\ttitle"
    rows = [header]
    for e in entries:
        rows.append("\t".join([
            e["id"], e["type"], e["group"], e["status"], e["issue"],
            "1" if e["in_table"] else "0", e["title"],
        ]))
    return "\n".join(rows)


def _fmt_json(entries: list[dict], missing_rows: list[str]) -> str:
    return json.dumps(
        {"entries": entries, "missing_from_table": sorted(missing_rows)},
        indent=2, ensure_ascii=False,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", default=DEFAULT_SOURCE,
                        help=f"handoff markdown path (default {DEFAULT_SOURCE})")
    parser.add_argument("--format", choices=["md", "tsv", "json"], default="md")
    parser.add_argument("--write-snapshot", metavar="PATH",
                        help="also write the TSV snapshot to PATH")
    parser.add_argument("--only-actionable", action="store_true",
                        help="omit Verified / Not applicable rows")
    parser.add_argument("--check", action="store_true",
                        help="report classification gaps and exit non-zero if any")
    args = parser.parse_args(argv)

    source = (ROOT / args.source) if not Path(args.source).is_absolute() else Path(args.source)
    if not source.exists():
        print(f"error: {source} not found (migrated to Backlog tasks; see "
              f"docs/project/MAC_PORT_QUEUE.tsv)", file=sys.stderr)
        return 2

    entries, missing_from_groups, extra_in_groups = extract(source)
    if args.only_actionable:
        entries = [e for e in entries if e["status"] in ACTIONABLE]

    # recompute the "headings missing from table" for the report view
    text = source.read_text(encoding="utf-8")
    table_ids = set(_parse_queue(text))
    missing_rows = [e["id"] for e in entries if e["id"] not in table_ids]

    if args.format == "tsv":
        print(_fmt_tsv(entries))
    elif args.format == "json":
        print(_fmt_json(entries, missing_rows))
    else:
        print(_fmt_markdown(entries, missing_rows))

    if args.write_snapshot:
        snap = Path(args.write_snapshot)
        if not snap.is_absolute():
            snap = ROOT / snap
        snap.parent.mkdir(parents=True, exist_ok=True)
        snap.write_text(_fmt_tsv(entries) + "\n", encoding="utf-8")
        print(f"wrote {snap.relative_to(ROOT)} ({len(entries)} rows)", file=sys.stderr)

    if args.check:
        ok = True
        if missing_rows:
            print(f"CHECK: headings missing from queue table: {', '.join(sorted(missing_rows))}",
                  file=sys.stderr)
            ok = False
        if missing_from_groups:
            print(f"CHECK: awaiting-validation entries with no group: "
                  f"{', '.join(missing_from_groups)}", file=sys.stderr)
            ok = False
        if extra_in_groups:
            print(f"CHECK: grouped IDs that are not actionable entries: "
                  f"{', '.join(extra_in_groups)}", file=sys.stderr)
            ok = False
        print("check: OK" if ok else "check: FAILED", file=sys.stderr)
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
