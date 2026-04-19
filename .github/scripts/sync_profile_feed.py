#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECENT_PATH = ROOT / "dashboards" / "recent.json"
PROFILE_README_PATH = (
    Path(os.environ.get("PROFILE_REPO_PATH", str(ROOT / "profile-repo"))) / "README.md"
)

ZH_AREA_MAP = {
    "Fitness": "健身",
    "Nutrition": "营养",
    "Planning": "规划",
    "Reading": "阅读",
    "System": "系统",
    "Learning": "学习",
    "Work": "工作",
    "Personal": "个人",
    "Ideas": "想法",
    "Project": "项目",
}


def load_items() -> list[dict]:
    with RECENT_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)[:6]


def render_en(items: list[dict]) -> str:
    lines = ["| Date | Area | Update |", "|:-----|:-----|:-----|"]
    for item in items:
        lines.append(
            f'| {item["date"]} | {item["emoji"]} {item["area"]} '
            f'| {item["summary"]} — [→]({item["link"]}) |'
        )
    return "\n".join(lines)


def render_zh(items: list[dict]) -> str:
    lines = ["| 日期 | 领域 | 动态 |", "|:-----|:-----|:-----|"]
    for item in items:
        area = ZH_AREA_MAP.get(item["area"], item["area"])
        lines.append(
            f'| {item["date"]} | {item["emoji"]} {area} '
            f'| {item["summary"]} — [→]({item["link"]}) |'
        )
    return "\n".join(lines)


def replace_block(content: str, start: str, end: str, block: str) -> str:
    pattern = re.compile(
        rf"({re.escape(start)})(.*?)(\s*{re.escape(end)})",
        flags=re.DOTALL,
    )

    def repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}\n{block}\n{match.group(3)}"

    updated, count = pattern.subn(repl, content, count=1)
    if count != 1:
        raise RuntimeError(f"Could not find marker pair: {start} ... {end}")
    return updated


def main() -> None:
    items = load_items()

    content = PROFILE_README_PATH.read_text(encoding="utf-8")
    content = replace_block(
        content,
        "<!-- WIKI-FEED:START -->",
        "<!-- WIKI-FEED:END -->",
        render_en(items),
    )
    content = replace_block(
        content,
        "<!-- WIKI-FEED-ZH:START -->",
        "<!-- WIKI-FEED-ZH:END -->",
        render_zh(items),
    )

    PROFILE_README_PATH.write_text(content, encoding="utf-8")
    print(f"Updated {PROFILE_README_PATH}")


if __name__ == "__main__":
    main()
