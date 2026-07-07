#!/usr/bin/env python3
"""Redact common PII from text or JSONL records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


PATTERNS = [
    (re.compile(r"1[3-9]\d{9}"), "[PHONE]"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[EMAIL]"),
    (re.compile(r"(微信|WeChat|wechat|VX|vx)[:：]?\s*[A-Za-z0-9_-]{5,}"), "[WECHAT]"),
    (re.compile(r"(QQ|qq)[:：]?\s*\d{5,12}"), "[QQ]"),
    (re.compile(r"\b\d{15}(\d{2}[0-9Xx])?\b"), "[ID_NUMBER]"),
    (re.compile(r"(学生|同学|申请人|案例主人公)?[：:]\s*[\u4e00-\u9fff]{2,4}(同学|学生)?"), r"\1: [NAME]"),
]


def redact_text(text: str) -> tuple[str, bool]:
    changed = False
    result = text
    for pattern, replacement in PATTERNS:
        result, count = pattern.subn(replacement, result)
        changed = changed or count > 0
    return result, changed


def redact_obj(obj: Any) -> tuple[Any, bool]:
    if isinstance(obj, str):
        return redact_text(obj)
    if isinstance(obj, list):
        changed = False
        values = []
        for item in obj:
            value, item_changed = redact_obj(item)
            values.append(value)
            changed = changed or item_changed
        return values, changed
    if isinstance(obj, dict):
        changed = False
        result = {}
        for key, value in obj.items():
            if key.lower() in {"name", "student_name", "phone", "email", "wechat", "avatar", "image"}:
                result[key] = "[REDACTED]"
                changed = True
            else:
                result[key], item_changed = redact_obj(value)
                changed = changed or item_changed
        result["pii_removed"] = True
        return result, True if changed else result.get("pii_removed", False)
    return obj, False


def main() -> int:
    parser = argparse.ArgumentParser(description="Redact common PII from plain text or JSONL.")
    parser.add_argument("input", nargs="?", help="Input file. Reads stdin if omitted.")
    parser.add_argument("--jsonl", action="store_true", help="Treat input as JSONL.")
    args = parser.parse_args()

    data = open(args.input, "r", encoding="utf-8").read() if args.input else sys.stdin.read()

    if args.jsonl:
        for line in data.splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            redacted, _ = redact_obj(obj)
            print(json.dumps(redacted, ensure_ascii=False, sort_keys=True))
    else:
        redacted, _ = redact_text(data)
        print(redacted, end="" if redacted.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
