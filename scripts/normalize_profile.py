#!/usr/bin/env python3
"""Normalize admissions profile JSON or JSONL records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


REGION_MAP = {
    "香港": "Hong Kong",
    "港": "Hong Kong",
    "新加坡": "Singapore",
    "英国": "UK",
    "英": "UK",
    "美国": "US",
    "美": "US",
    "加拿大": "Canada",
    "澳洲": "Australia",
    "澳大利亚": "Australia",
    "欧洲": "Europe",
}


def normalize_region(text: str | None) -> str | None:
    if not text:
        return None
    for key, value in REGION_MAP.items():
        if key in text:
            return value
    return text


def normalize_tier(text: str | None) -> str:
    if not text:
        return "unknown"
    lowered = text.lower()
    if "c9" in lowered:
        return "C9"
    if "985" in lowered:
        return "985"
    if "211" in lowered:
        return "211"
    if "双一流" in text or "double first" in lowered:
        return "double-first-class"
    if "海本" in text or "overseas" in lowered:
        return "overseas"
    if "双非" in text or "普通" in text:
        return "regular-mainland"
    return text


def normalize_gpa(text: str | None) -> float | None:
    if not text:
        return None
    match = re.search(r"(?<!\d)([6-9]\d(?:\.\d+)?)(?:\s*/\s*100)?(?!\d)", text)
    if match:
        return float(match.group(1))
    match = re.search(r"([2-4](?:\.\d+)?)\s*/\s*4(?:\.0)?", text)
    if match:
        return round(float(match.group(1)) / 4.0 * 100, 2)
    match = re.search(r"([2-4](?:\.\d+)?)\s*/\s*5(?:\.0)?", text)
    if match:
        return round(float(match.group(1)) / 5.0 * 100, 2)
    return None


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    result = dict(record)
    combined_region = " ".join(str(result.get(k, "")) for k in ("target_region", "admitted_school", "admitted_program"))
    result["target_region"] = normalize_region(result.get("target_region") or combined_region)
    result["undergraduate_school_tier"] = normalize_tier(result.get("undergraduate_school_tier"))
    result["gpa_normalized"] = result.get("gpa_normalized") or normalize_gpa(result.get("gpa_text"))
    tags = set(result.get("tags") or [])
    if result.get("gpa_normalized") is None:
        tags.add("gpa_unknown")
    result["tags"] = sorted(tags)
    return result


def load_records(data: str, jsonl: bool) -> list[dict[str, Any]]:
    if jsonl:
        return [json.loads(line) for line in data.splitlines() if line.strip()]
    parsed = json.loads(data)
    return parsed if isinstance(parsed, list) else [parsed]


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize admissions case profile records.")
    parser.add_argument("input", nargs="?", help="Input JSON or JSONL. Reads stdin if omitted.")
    parser.add_argument("--jsonl", action="store_true", help="Read and write JSONL.")
    args = parser.parse_args()

    data = open(args.input, "r", encoding="utf-8").read() if args.input else sys.stdin.read()
    records = [normalize_record(record) for record in load_records(data, args.jsonl)]

    if args.jsonl:
        for record in records:
            print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    else:
        print(json.dumps(records[0] if len(records) == 1 else records, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
