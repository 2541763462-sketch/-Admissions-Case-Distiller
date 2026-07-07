# Recommendation Framework

## Inputs

Use:
- Student profile supplied by the user.
- Public, attributable statements from study-abroad agencies.
- Public, attributable admissions cases from study-abroad agencies.
- Official program requirements.
- Similar anonymous cases from the JSONL database.

Do not infer protected or sensitive attributes.

## Output Structure

For a full applicant analysis, first show the analysis structure, then the analysis, then references at the end. Do not start with references.

Recommended order:
1. Analysis structure
2. Background positioning and core judgment
3. Region and discipline strategy
4. Programme tiering and application portfolio
5. Improvement plan and essay story line
6. Similar-background application references and source notes

Keep the "Similar-background application references" section in table form:

| 来源 | 相似案例 | 背景信号 | 录取结果 | 对你的参考 |
|---|---|---|---|---|

The "对你的参考" column should be substantive. Explain what the case implies for school tier, language threshold, soft-background packaging, major-switch risk, project selection, and what the applicant should copy or avoid strategically. Do not merely say "similar" or "can refer to it."

## School Tier Labels

Use qualitative labels:
- Reach: plausible but competitive; several gaps or high selectivity.
- Target: profile matches multiple public-case signals and official requirements.
- Safer: requirements are met with fewer obvious gaps.

Avoid exact admission probabilities unless the user has a calibrated dataset.

## Evidence Rules

All judgments must be evidence-grounded. Do not make generic counselling claims without tying them to public cases, public agency statements, official programme requirements, or the user's stated profile.

Tie advice to evidence:
- "Based on similar anonymous cases with 985 finance backgrounds and IELTS 7.0..."
- "Based on official program requirements..."
- "Based on the public agency case where a 211 Chinese-language applicant with IELTS 7.0 received..."
- "Based on the user's stated internship history..."

Use evidence levels:
- **Official requirement**: university programme pages, tuition pages, English-language requirements, deadlines, portfolio/writing-sample requirements.
- **Public agency case**: public admission case pages from configured agencies. Use for directional applicant-background comparison only.
- **Public agency commentary**: public articles or posts from agencies about admission preferences, portfolio advice, interview tendencies, or project difficulty. Treat as interpretive, not official.
- **User profile evidence**: the applicant's GPA, tests, internships, projects, awards, and preferences.
- **Inference from evidence**: allowed only when explicitly named as inference and linked to the evidence above.

When evidence is weak or missing:
- Say "公开案例不足以支撑强判断" or "未找到足够相似的公开案例".
- Use cautious language such as "directionally suggests", "可作为参考", "更像匹配层", or "需要复核".
- Do not fill gaps with confident-sounding admissions folklore.

Avoid:
- "You will get in."
- "This school is guaranteed."
- "The agency case proves..."
- "This programme prefers..." unless an official page or public agency commentary actually says so.
- "This background is enough..." unless similar public cases and official requirements support that claim.

## Similar Case Search Rules

When searching public agency cases, use a broad-to-narrow sequence:
1. Same undergraduate institution.
2. Same institution tier and score band.
3. Same language score band.
4. Same target region.
5. Same or adjacent discipline.
6. Similar soft-background pattern.

Use at least three source families when available. Good source diversity:
- CompassEdu / 指南者
- New Oriental / 新东方前途出国
- EIC / 启德
- JJL / 金吉列
- Official university pages

If exact school matches exist from only one source, use those for high-similarity anchors, then add adjacent matches from other agencies with the same score band and target region.

Do not overfit cases. Public cases are marketing-selected and incomplete. Use them to infer directional signals, not probabilities.

## Claim Discipline

For every major recommendation, be able to answer:
- Which public case, agency statement, official page, or user-profile fact supports this?
- Is this a requirement, an observed case pattern, or an inference?
- Is the case close enough by school tier, score band, language score, region, discipline, and experience type?
- Does the recommendation need a caveat because public cases are sparse or marketing-selected?

If a recommendation cannot pass this check, either remove it or label it as a low-confidence hypothesis.

## Action Plan

Prioritize by time-to-impact:
- High impact, near term: language score, prerequisite course proof, resume restructuring, recommendation strategy.
- Medium term: research project, internship depth, portfolio, quantitative project.
- Long term: publication, major career pivot, extensive additional coursework.
