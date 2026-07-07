---
name: admissions-case-distiller
description: Use when building or operating a compliant background admissions case distiller for publicly accessible overseas master's application cases from study-abroad agencies, university pages, or user-authorized materials. The skill supports no-login public case discovery, cautious crawling, anonymized field extraction, profile normalization, similarity analysis, school-positioning advice, and essay-feedback coaching. Do not use it to bypass login, captcha, paywalls, anti-bot systems, robots.txt, access controls, or to copy proprietary essays or store personally identifying student data.
---

# Admissions Case Distiller

## Purpose

This skill builds and operates a compliant public admissions-case insight pipeline for Chinese students applying to overseas master's programs. It may collect public, no-login case pages and convert them into anonymous structured facts for school positioning, background-improvement advice, and essay coaching.

The goal is to distill patterns, not copy content.

## Hard Boundaries

Allowed:
- Public pages that require no login, no payment, no captcha, and no access circumvention.
- Pages permitted by robots.txt and source terms when available.
- User-owned or user-authorized application materials.
- Official university pages and public program requirement pages.
- Short summaries, anonymous extracted fields, source URLs, crawl timestamps, and derived statistics.

Disallowed:
- Login, session cookies, paid accounts, private APIs, captcha solving, browser stealth, IP rotation, or anti-bot bypass.
- Ignoring robots.txt or crawling pages explicitly disallowed for the configured user agent.
- Storing names, avatars, contact details, full CVs, full essays, screenshots of students, or uniquely identifying personal stories.
- Reproducing source article text, copying proprietary essays, or rewriting another student's essay as a new essay.
- Presenting public cases as guaranteed admission outcomes.

If a user asks for stealth crawling, login bypass, high-volume scraping, or essay copying, refuse that part and offer the compliant public-case pipeline.

## Workflow

1. Define sources in a registry.
2. Check robots.txt for each source before fetching.
3. Discover likely case URLs from configured entry pages.
4. Fetch only public HTML pages at a low rate.
5. Skip login, captcha, paywall, blocked, or non-case pages.
6. Extract anonymous fields into the profile schema.
7. Redact PII and remove raw article bodies before storage.
8. Normalize GPA, school tiers, target regions, majors, and program names.
9. Deduplicate similar cases.
10. Generate advice from aggregate patterns and similar anonymous profiles.

Use `scripts/crawl_cases.py` for steps 2-7. Use `scripts/normalize_profile.py`, `scripts/redact_pii.py`, and `scripts/score_fit.py` for focused operations.

## Source Registry

Create a JSON file such as `sources.json`:

```json
{
  "user_agent": "AdmissionsCaseDistiller/0.1 (+contact@example.com)",
  "output_jsonl": "cases.jsonl",
  "max_pages_per_source": 20,
  "request_delay_seconds": 5,
  "sources": [
    {
      "name": "Example Agency",
      "entry_urls": ["https://www.example.com/cases/"],
      "include_url_keywords": ["case", "offer", "录取", "案例", "成功案例"],
      "exclude_url_keywords": ["login", "signin", "member", "pay", "course"]
    }
  ]
}
```

Then run:

```bash
python3 scripts/crawl_cases.py sources.json
```

The crawler writes JSONL records with source URL, extracted fields, redaction flags, and brief non-verbatim summaries. It does not store full HTML or full article text.

## Profile Schema

Read `references/profile-schema.md` before changing extraction fields or storage format.

Core fields:
- `source_name`
- `source_url`
- `crawled_at`
- `case_year`
- `target_region`
- `admitted_school`
- `admitted_program`
- `undergraduate_school_tier`
- `undergraduate_major`
- `gpa_text`
- `gpa_normalized`
- `language_score`
- `gre_gmat`
- `internship_summary`
- `research_summary`
- `competition_or_project_summary`
- `result_type`
- `tags`
- `pii_removed`
- `extraction_confidence`

Never store raw essays or full articles in this schema.

## Extraction Guidance

Read `references/extraction-rubric.md` when tuning extraction quality.

Prefer structured facts:
- "本科 985，金融专业，均分 87，IELTS 7.0，2段券商实习，录取港大金融硕士"

Avoid source prose:
- Long marketing paragraphs
- Student names
- Agency consultant comments copied verbatim
- Complete personal statement passages

When confidence is low, keep fields empty and add `needs_review` to `tags`.

## Recommendation Guidance

Read `references/recommendation-framework.md` before generating applicant advice.
Read `references/report-template.md` before producing a full applicant analysis report.
Read `references/html-report.md` when the user asks for an HTML report, printable report, visual report, designed report, or says to use the Reading Room / beautiful-feishu-whiteboard style.

All applicant judgments must be evidence-grounded. Use public agency cases, public agency commentary, official programme pages, and user-provided profile facts. If evidence is insufficient, say so and lower confidence. Do not provide generic admissions counselling as if it were case-based analysis.

Advice should include:
- Positioning: reach, target, safer categories.
- Evidence: which anonymous patterns or official program requirements support the advice.
- Weaknesses: academic, language, quantitative preparation, internship, research, story fit.
- Action plan: concrete next steps by priority.
- Uncertainty: explain limits of public-case data.

When the user asks for similar-case references, use multiple source families when available:
- Public agency case libraries configured in `sample-sources.json`, such as CompassEdu, New Oriental, EIC, and JJL.
- Official university programme pages for current requirements, tuition, language thresholds, and fit constraints.
- User-provided or locally crawled anonymous JSONL case records.

Do not rely on one agency source unless the search genuinely finds no relevant alternatives. If only one source has close matches, say that explicitly and add broader adjacent matches from other sources.

Do not claim an admission probability as fact unless the user provides a calibrated internal dataset. Use cautious labels such as high fit, moderate fit, stretch, or risky.

## Essay Coaching

Read `references/essay-feedback-rubric.md` before reviewing essays.

Allowed:
- Structure feedback
- Authenticity checks
- Program-fit analysis
- Evidence and specificity suggestions
- Topic selection and material mining
- Plagiarism-risk warnings

Disallowed:
- Copying or paraphrasing public essays
- Reusing another student's story arc as a template
- Fabricating experiences
- Writing a final essay that masks borrowed source material

## Compliance Checklist

Read `references/compliance.md` when adding a new data source, increasing crawl volume, or changing what is stored.

Before every crawl:
- Use a clear user agent.
- Check robots.txt.
- Use low request rates.
- Do not send login cookies.
- Do not attempt blocked URLs repeatedly.
- Store source URL and crawl time.
- Store anonymous structured fields only.

## Scripts

- `scripts/crawl_cases.py`: compliant public-page crawler and extractor.
- `scripts/redact_pii.py`: removes common Chinese/English PII from text or JSONL records.
- `scripts/normalize_profile.py`: normalizes profile JSON/JSONL fields.
- `scripts/score_fit.py`: compares an applicant profile with stored anonymous cases.

All scripts use Python standard library only.

## Assets

- `assets/html-report-template/reading-room-report.html`: reusable static HTML report skeleton using the Reading Room visual style adapted from `beautiful-feishu-whiteboard`.
