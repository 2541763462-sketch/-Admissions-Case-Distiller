#!/usr/bin/env python3
"""Score similarity between one applicant profile and anonymous case records."""

from __future__ import annotations

import argparse
import json
import math
from typing import Any


def tokens(value: Any) -> set[str]:
    text = str(value or "").lower()
    for ch in ",.;:/|()[]{}，。；：、（）【】":
        text = text.replace(ch, " ")
    return {part for part in text.split() if part}


def score(applicant: dict[str, Any], case: dict[str, Any]) -> float:
    total = 0.0
    weight = 0.0

    pairs = [
        ("target_region", 2.0),
        ("undergraduate_school_tier", 1.5),
        ("undergraduate_major", 1.0),
        ("admitted_program", 1.0),
    ]
    for key, item_weight in pairs:
        weight += item_weight
        a = tokens(applicant.get(key))
        b = tokens(case.get(key))
        if a and b:
            total += item_weight * (len(a & b) / len(a | b))

    weight += 1.5
    applicant_gpa = applicant.get("gpa_normalized")
    case_gpa = case.get("gpa_normalized")
    if isinstance(applicant_gpa, (int, float)) and isinstance(case_gpa, (int, float)):
        total += 1.5 * max(0.0, 1.0 - abs(applicant_gpa - case_gpa) / 20.0)

    weight += 1.0
    applicant_lang = tokens(applicant.get("language_score"))
    case_lang = tokens(case.get("language_score"))
    if applicant_lang and case_lang:
        total += 1.0 * (len(applicant_lang & case_lang) / len(applicant_lang | case_lang))

    return round(total / weight, 4) if weight else 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description="Find similar anonymous admissions cases.")
    parser.add_argument("applicant_json", help="Applicant profile JSON file.")
    parser.add_argument("cases_jsonl", help="Anonymous cases JSONL file.")
    parser.add_argument("--top", type=int, default=10, help="Number of matches to return.")
    args = parser.parse_args()

    with open(args.applicant_json, "r", encoding="utf-8") as handle:
        applicant = json.load(handle)

    matches = []
    with open(args.cases_jsonl, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            case = json.loads(line)
            matches.append((score(applicant, case), case))

    for value, case in sorted(matches, key=lambda item: item[0], reverse=True)[: args.top]:
        print(json.dumps({
            "similarity": value,
            "source_url": case.get("source_url"),
            "admitted_school": case.get("admitted_school"),
            "admitted_program": case.get("admitted_program"),
            "undergraduate_school_tier": case.get("undergraduate_school_tier"),
            "gpa_normalized": case.get("gpa_normalized"),
            "language_score": case.get("language_score"),
            "tags": case.get("tags", []),
        }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
