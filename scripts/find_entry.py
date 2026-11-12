"""Search or extract exact entries from the bundled Markdown book."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "sources" / "book"
HEAD = re.compile(r"(?m)^### (\d+)\. (.+)$")
FIELDS = ("成本", "说人话", "收益", "证据等级", "来源", "备注")


def entries():
    for path in sorted(BOOK.glob("[0-9][0-9]-*.md")):
        section = int(path.name[:2])
        body = path.read_text(encoding="utf-8")
        matches = list(HEAD.finditer(body))
        for idx, match in enumerate(matches):
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
            yield {
                "section": section,
                "item": int(match.group(1)),
                "title": match.group(2),
                "text": body[match.start() : end].strip(),
                "path": path,
                "line": body.count("\n", 0, match.start()) + 1,
            }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Search titles and full entry text")
    parser.add_argument("--section", type=int, help="Section number 1–34")
    parser.add_argument("--item", type=int, help="Exact item within a section")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--check", action="store_true", help="Audit fields and numbering")
    args = parser.parse_args()
    if not (args.query or args.section or args.check):
        parser.print_help()
        return 2

    all_entries = list(entries())
    if args.check:
        problems = []
        sections = {}
        for entry in all_entries:
            sections.setdefault(entry["section"], []).append(entry["item"])
            for field in FIELDS:
                if not re.search(rf"(?m)^- {field}：", entry["text"]):
                    problems.append(f'{entry["section"]}.{entry["item"]}: missing {field}')
            if "<!-- 成本标签:" not in entry["text"]:
                problems.append(f'{entry["section"]}.{entry["item"]}: missing cost tag')
        for section, numbers in sections.items():
            if numbers != list(range(1, len(numbers) + 1)):
                problems.append(f"section {section}: nonsequential item numbers")
        if len(sections) != 34 or len(all_entries) != 767:
            problems.append(f"unexpected corpus size: {len(sections)} sections, {len(all_entries)} entries")
        print(f"sections={len(sections)} entries={len(all_entries)} problems={len(problems)}")
        for problem in problems:
            print(problem)
        return 1 if problems else 0

    if args.item is not None:
        if args.section is None:
            parser.error("--item requires --section")
        for entry in all_entries:
            if entry["section"] == args.section and entry["item"] == args.item:
                print(f'{entry["path"]}:{entry["line"]}\n{entry["text"]}')
                return 0
        print("Entry not found", file=sys.stderr)
        return 1

    if args.query:
        needle = args.query.casefold()
        hits = [e for e in all_entries if needle in e["text"].casefold()]
        hits.sort(key=lambda e: (needle not in e["title"].casefold(), e["section"], e["item"]))
        for entry in hits[: max(0, args.limit)]:
            print(f'{entry["section"]}.{entry["item"]} {entry["title"]} — {entry["path"]}:{entry["line"]}')
        print(f"matches={len(hits)} shown={min(len(hits), max(0, args.limit))}")
        return 0

    for entry in all_entries:
        if entry["section"] == args.section:
            print(f'{entry["section"]}.{entry["item"]} {entry["title"]} — {entry["path"]}:{entry["line"]}')
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
