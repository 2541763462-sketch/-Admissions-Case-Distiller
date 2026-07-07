# HTML Report Reference

Use this when the user asks for:
- an HTML report
- a printable report
- a visual report
- a designed report
- a report using `beautiful-feishu-whiteboard`
- a report using the Reading Room style

## Default Style

Use the `Reading Room` visual style adapted from `beautiful-feishu-whiteboard`.

Palette:
- canvas: `#F6EBD8`
- ink: `#0B0A09`
- lilac: `#D6C7CC`
- terracotta: `#DE916A`
- butter: `#F1DAB1`
- cream panel: `#FFF8ED`

Design rules:
- quiet literary-editorial tone
- cream paper background
- thin black rectangular borders
- squared corners
- no shadows
- no gradients
- generous whitespace
- large strong title
- pastel blocks for emphasis
- tables for evidence and case references

## Template Asset

Start from:

```text
assets/html-report-template/reading-room-report.html
```

Copy it to a user-facing file in the workspace and replace the content. Do not overwrite the template asset unless the user asks to modify the skill template itself.

Suggested filename:

```text
<student-school>-<major>-<regions>-admissions-report.html
```

Use lowercase pinyin or English slugs where possible.

## Content Requirements

The HTML report should follow the compact report structure:

1. Hero summary
2. Background positioning and core judgment
3. Region and discipline strategy
4. Programme tiering and application portfolio
5. Improvement plan and essay story line
6. Similar-background application references and sources
7. Visual decision charts

Preserve the full written analysis. Do not replace narrative sections with charts. Charts are an end-of-report visual summary only.

For evidence-grounded reports:
- show evidence tags such as public case, official requirement, agency commentary, user profile, or inference
- keep all major claims traceable to a source or user fact
- put official pages and public case links at the end
- include caveats when the application season is in the future

Keep the similar-case table format:

```markdown
| 来源 | 相似案例 | 背景信号 | 录取结果 | 对你的参考 |
|---|---|---|---|---|
```

## HTML Constraints

Create a single static `.html` file:
- no external JavaScript
- no external CSS
- no remote fonts
- links may point to public sources
- responsive layout for desktop and mobile
- print-friendly CSS
- use semantic headings, tables, and lists

If the report is long, prefer clear sections and tables over dense paragraphs.

## End Charts

Append charts at the end of the report when useful. Recommended static HTML/CSS charts:
- Direction fit bar chart
- Project portfolio matrix
- Story-line pathway
- Risk/priority matrix

Do not use external chart libraries. Build charts with semantic HTML, CSS grid, bordered boxes, and simple bars so the file remains standalone and printable.

Chart values should be labelled as directional assessment, not probabilities. Tie them back to the written analysis and evidence caveats.

## Verification

After writing the file:
- check that the file exists
- check the title
- count tables and links when useful
- provide the absolute file link to the user
- also provide the report's key written analysis in the chat response, not only the file link
- include the compact text version with the same main sections: background positioning, region/discipline strategy, programme portfolio, improvement/story line, similar-case evidence summary
- keep the chat version concise when the HTML is long, but make sure the user can read the core reasoning without opening the file

Do not start a dev server for a static HTML report.
