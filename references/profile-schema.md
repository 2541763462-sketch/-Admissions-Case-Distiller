# Profile Schema

## JSONL Record

Each line in the case database is one JSON object.

```json
{
  "source_name": "Example Agency",
  "source_url": "https://www.example.com/case/123",
  "crawled_at": "2026-07-07T12:00:00+08:00",
  "case_year": "2025",
  "target_region": "Hong Kong",
  "admitted_school": "University of Hong Kong",
  "admitted_program": "MSc Finance",
  "undergraduate_school_tier": "985",
  "undergraduate_major": "Finance",
  "gpa_text": "87/100",
  "gpa_normalized": 87.0,
  "language_score": "IELTS 7.0",
  "gre_gmat": "GMAT 700",
  "internship_summary": "2 finance-related internships",
  "research_summary": "1 course research project",
  "competition_or_project_summary": "",
  "result_type": "admit",
  "tags": ["business", "hong-kong"],
  "pii_removed": true,
  "extraction_confidence": 0.72
}
```

## Field Notes

- `target_region`: normalize to values such as Hong Kong, Singapore, UK, US, Canada, Australia, Europe, Other.
- `undergraduate_school_tier`: use C9, 985, 211, double-first-class, regular-mainland, overseas, unknown.
- `gpa_normalized`: use 100-point scale where possible; leave null if unsafe.
- `internship_summary`: keep coarse counts and industry only.
- `research_summary`: keep coarse counts and domain only.
- `tags`: include domain, source quality, `needs_review`, `low_confidence`, or `official_program` as appropriate.

## Privacy Rule

If a fact is unusually specific and could identify the applicant, generalize or remove it. For example, change "interned at Company X in Team Y under Manager Z" to "one related industry internship".
