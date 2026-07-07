# Extraction Rubric

## Page Classification

Likely admissions case pages include terms such as:
- 录取案例
- 成功案例
- offer
- 案例库
- 申请案例
- 硕士申请
- 研究生申请
- 背景
- GPA
- 雅思
- 托福
- GRE
- GMAT

Skip pages dominated by:
- 课程销售
- 顾问介绍
- 登录注册
- 支付
- 留资表单
- 新闻转载

## Field Extraction

Extract only concise factual fields. If a value is ambiguous, leave it empty and add `needs_review`.

Useful patterns:
- GPA: `GPA 3.6/4.0`, `均分 87`, `绩点 3.5`
- Language: `IELTS 7.0`, `雅思 7`, `TOEFL 105`, `托福 105`
- Tests: `GRE 325`, `GMAT 700`
- School tier: `985`, `211`, `双一流`, `海本`, `C9`
- Admit result: `录取`, `offer`, `con`, `unconditional`

## Confidence

Start at 0.3 for a page classified as a case.

Add:
- +0.1 for admitted school
- +0.1 for admitted program
- +0.1 for GPA or grade
- +0.1 for language score
- +0.1 for undergraduate tier or school signal
- +0.1 for internship/research signal

Cap at 0.9. Use 0.0 if the page is not a case.

## Summary Style

Good:
- "985 finance background, 87 average, IELTS 7.0, finance internship experience, admitted to Hong Kong business master's program."

Bad:
- Long copied paragraphs from the source.
- Student-specific life stories.
- Consultant marketing language.
