# Admissions Case Distiller

一个面向留学申请咨询场景的 Codex Skill：基于**公开留学机构案例、公开机构观点、学校官方项目要求**和**用户授权背景信息**，生成境外硕士申请定位、项目组合、背景提升、文书主线和可视化 HTML 报告。
首次使用输入：使用 admissions-case-distiller，帮我基于公开留学机构案例、官方项目要求和我的背景，做一份证据化的境外硕士申请定位分析。请不要空谈，每个关键判断都尽量对应公开案例、机构观点或官方要求；如果证据不足请明确说明。最后请生成一份 Reading Room 风格的 HTML 报告，并在这里同步展示核心文字分析。

我的背景如下：
- 本科院校/层级：
- 本科专业：
- GPA/均分：
- 语言成绩：
- GRE/GMAT：
- 实习经历：
- 科研/项目/竞赛：
- 目标地区：
- 目标专业：
- 申请季：
- 偏好/限制：预算、城市、排名、就业方向等

- 下图为示例
<img width="1600" height="4983" alt="image" src="https://github.com/user-attachments/assets/a1d8bccd-36ce-4e8a-90b1-ba5173f9f9da" />

它的目标不是复制案例库，而是把公开案例蒸馏成可追溯、匿名化、证据化的申请判断。

## 能做什么

- 抓取无需登录、无需验证码、无需付费的公开申请案例页面。
- 检查 `robots.txt`，低频访问，不绕过访问限制。
- 从公开案例中提取匿名结构化字段。
- 对学生背景做标准化分析。
- 基于公开案例和官方项目要求生成申请定位。
- 输出冲刺 / 主申 / 稳妥项目组合。
- 生成文书故事线逻辑框架。
- 生成 Reading Room 风格的静态 HTML 报告。
- 在报告末尾追加可视化决策图表。

## 不做什么

本 Skill 明确禁止：

- 登录抓取、Cookie 复用、验证码绕过、付费墙绕过。
- 使用代理池、浏览器 stealth、反爬绕过。
- 存储学生姓名、联系方式、头像、完整 CV、完整文书。
- 复制或改写留学机构原文案例。
- 把公开案例当作录取保证。
- 在证据不足时做确定性判断。

## 目录结构

```text
admissions-case-distiller/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── html-report-template/
│       └── reading-room-report.html
├── references/
│   ├── compliance.md
│   ├── essay-feedback-rubric.md
│   ├── extraction-rubric.md
│   ├── html-report.md
│   ├── profile-schema.md
│   ├── recommendation-framework.md
│   └── report-template.md
├── scripts/
│   ├── crawl_cases.py
│   ├── normalize_profile.py
│   ├── redact_pii.py
│   └── score_fit.py
└── sample-sources.json
```

## 数据源配置

编辑 `sample-sources.json`：

```json
{
  "user_agent": "AdmissionsCaseDistiller/0.1 (+your-email@example.com)",
  "output_jsonl": "cases.jsonl",
  "max_pages_per_source": 30,
  "request_delay_seconds": 5,
  "sources": [
    {
      "name": "指南者留学",
      "entry_urls": ["https://m.compassedu.hk/offer/0/1"],
      "include_url_keywords": ["offer", "录取", "案例", "硕士"],
      "exclude_url_keywords": ["login", "member", "pay", "register"]
    }
  ]
}
```

建议使用真实联系邮箱作为 `user_agent` 的一部分，便于站点管理员联系。

## 运行公开案例采集

```bash
cd admissions-case-distiller
python3 scripts/crawl_cases.py sample-sources.json
```

输出为 JSONL，每一行是一条匿名化案例记录。

## 脱敏

```bash
python3 scripts/redact_pii.py cases.jsonl --jsonl > cases.redacted.jsonl
```

会脱敏常见手机号、邮箱、微信、QQ、身份证号等信息，并标记 `pii_removed`。

## 归一化

```bash
python3 scripts/normalize_profile.py cases.redacted.jsonl --jsonl > cases.normalized.jsonl
```

会标准化地区、院校层级、GPA 等字段。

## 相似案例匹配

准备一个学生背景 JSON：

```json
{
  "target_region": "Hong Kong",
  "undergraduate_school_tier": "211",
  "undergraduate_major": "English",
  "gpa_normalized": 90,
  "language_score": "IELTS 6.5",
  "admitted_program": "Communication"
}
```

运行：

```bash
python3 scripts/score_fit.py applicant.json cases.normalized.jsonl --top 10
```

## 报告输出规则

完整申请报告默认使用 5 个主体板块：

1. 背景定位与核心判断
2. 地区与专业策略
3. 项目分层与申请组合
4. 提升方案与文书主线
5. 相似背景申请参考与资料来源

如果生成 HTML 报告，会额外在最后追加：

6. 可视化决策图表

HTML 报告使用 `beautiful-feishu-whiteboard` 的 Reading Room 风格改造：

- 奶油纸底
- 细黑线框
- 柔和色块
- 静态单文件 HTML
- 无外部 JS/CSS
- 支持移动端和打印

模板位于：

```text
assets/html-report-template/reading-room-report.html
```

## 证据要求

所有判断必须落到证据上。证据类型包括：

- 官方项目要求
- 留学机构公开真实案例
- 留学机构公开观点 / 解读
- 用户提供的背景事实
- 明确标注的基于证据推断

如果证据不足，应明确写：

```text
公开案例不足以支撑强判断。
未找到足够相似的公开案例。
该建议为低置信度推断。
```

## 相似案例表格格式

报告中的相似案例部分固定使用：

```markdown
| 来源 | 相似案例 | 背景信号 | 录取结果 | 对你的参考 |
|---|---|---|---|---|
```

要求：

- 尽量跨多个机构来源。
- 优先使用同校、同院校层级、同分数段案例。
- 区分强参考、邻近参考、弱参考。
- 不把案例当作录取保证。

## 文书主线框架

多方向申请者会生成可切换的逻辑框架，而不是默认写完整文书。覆盖文科、商科、工科、理科、数据、法律和公共政策等方向：

- 应用语言 / 专业英语
- 传播 / IMC / 媒体
- Marketing / Brand Management
- Marketing Analytics / Consumer Insight
- 语言教育 / TESL
- 金融 / 会计 / 投资
- 管理 / 战略 / 创业
- Business Analytics / Data Science / Information Systems
- Computer Science / Software Engineering / AI
- Engineering / Built Environment / Industrial Technology
- Science / Research / Lab-based Programmes
- Social Science / Public Policy / International Affairs
- Law / Compliance / IP / Governance

通用母线示例：

```text
Language → Communication → Brand → Consumer Insight
Accounting → Valuation → Investment Judgment → Capital Allocation
Business Problem → Data Method → Decision Insight → Operational Impact
Coursework → Technical Project → Industry Constraint → Engineering Solution
Research Question → Method → Evidence → Future Inquiry
Social Observation → Policy Evidence → Institutional Analysis → Public Impact
Rules → Risk → Governance → Responsible Innovation
```

## 合规声明

公开可访问不等于可以无限制抓取和复用。本 Skill 只做公开、低频、可追溯、匿名化、结构化的事实提取与趋势分析；不保存原文资产，不收集个人身份信息，不绕过访问限制。

## 许可证

请根据你的仓库策略自行添加许可证。若用于商业场景，建议在部署前进行法律、隐私和数据合规审查。
