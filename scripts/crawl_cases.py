#!/usr/bin/env python3
"""Crawl public, no-login admissions case pages into anonymous JSONL records.

Config format is documented in ../SKILL.md. This script uses only Python's
standard library and intentionally avoids login, cookies, browser automation,
captcha solving, or anti-bot bypass.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from typing import Any


CASE_KEYWORDS = ["录取案例", "成功案例", "申请案例", "案例库", "offer", "硕士申请", "研究生申请", "背景", "GPA", "雅思", "托福"]
BLOCK_KEYWORDS = ["登录", "注册", "验证码", "captcha", "access denied", "付费", "会员", "请先登录"]
DEFAULT_USER_AGENT = "AdmissionsCaseDistiller/0.1"


class LinkTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.text_parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip += 1
            return
        if tag == "a":
            for key, value in attrs:
                if key.lower() == "href" and value:
                    self.links.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            cleaned = " ".join(html.unescape(data).split())
            if cleaned:
                self.text_parts.append(cleaned)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def load_config(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def can_fetch(url: str, user_agent: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
        return parser.can_fetch(user_agent, url)
    except Exception:
        return True


def fetch(url: str, user_agent: str, timeout: int = 20) -> str | None:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type and "application/xhtml" not in content_type:
                return None
            raw = response.read(2_000_000)
            charset = response.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")
    except Exception:
        return None


def parse_html(page: str) -> tuple[str, list[str]]:
    parser = LinkTextParser()
    parser.feed(page)
    text = " ".join(parser.text_parts)
    text = re.sub(r"\s+", " ", text)
    return text[:50000], parser.links


def absolute_url(base: str, href: str) -> str | None:
    if href.startswith(("javascript:", "mailto:", "tel:", "#")):
        return None
    value = urllib.parse.urljoin(base, href)
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        return None
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", parsed.query, ""))


def looks_like_case(url: str, text: str, include_keywords: list[str]) -> bool:
    haystack = f"{url} {text[:5000]}".lower()
    keywords = CASE_KEYWORDS + include_keywords
    return sum(1 for keyword in keywords if keyword.lower() in haystack) >= 2


def looks_blocked(text: str) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in BLOCK_KEYWORDS)


def first_match(patterns: list[str], text: str) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            return " ".join(group for group in match.groups() if group).strip()
    return None


def normalize_region(text: str | None) -> str | None:
    if not text:
        return None
    mapping = {
        "香港": "Hong Kong",
        "港大": "Hong Kong",
        "港中文": "Hong Kong",
        "港科技": "Hong Kong",
        "新加坡": "Singapore",
        "英国": "UK",
        "美国": "US",
        "加拿大": "Canada",
        "澳洲": "Australia",
        "澳大利亚": "Australia",
    }
    for key, value in mapping.items():
        if key in text:
            return value
    return None


def normalize_gpa(text: str | None) -> float | None:
    if not text:
        return None
    match = re.search(r"([2-4](?:\.\d+)?)\s*/\s*4(?:\.0)?", text)
    if match:
        return round(float(match.group(1)) / 4.0 * 100, 2)
    match = re.search(r"([2-4](?:\.\d+)?)\s*/\s*5(?:\.0)?", text)
    if match:
        return round(float(match.group(1)) / 5.0 * 100, 2)
    match = re.search(r"(?<!\d)([6-9]\d(?:\.\d+)?)(?:\s*/\s*100)?(?!\d)", text)
    if match:
        return float(match.group(1))
    return None


def summarize_experience(text: str, keywords: list[str]) -> str:
    if not any(keyword in text for keyword in keywords):
        return ""
    count_match = None
    for keyword in keywords:
        for match in re.finditer(re.escape(keyword), text):
            start = max(0, match.start() - 12)
            end = min(len(text), match.end() + 12)
            window = text[start:end]
            before = text[start:match.start()]
            counts = list(re.finditer(r"([一二三四五六七八九两\d]+)\s*(?:段|份|个|项)", before))
            count_match = counts[-1] if counts else re.search(r"([一二三四五六七八九两\d]+)\s*(?:段|份|个|项)", window)
            if count_match:
                break
        if count_match:
            break
    count = count_match.group(1) if count_match else None
    count_map = {"一": "1", "二": "2", "两": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
    count = count_map.get(count, count)
    domains = []
    domain_words = {
        "finance": ["金融", "券商", "投行", "银行", "证券", "基金"],
        "data": ["数据", "商业分析", "机器学习", "算法"],
        "computer-science": ["计算机", "软件", "开发", "编程"],
        "media": ["传媒", "媒体", "传播"],
        "education": ["教育", "教学"],
        "consulting": ["咨询", "战略"],
    }
    for label, words in domain_words.items():
        if any(word in text for word in words):
            domains.append(label)
    pieces = []
    if count:
        pieces.append(f"{count} related experience item(s)")
    else:
        pieces.append("related experience mentioned")
    if domains:
        pieces.append("domains: " + ", ".join(domains[:3]))
    return "; ".join(pieces)


def redact_inline(text: str) -> tuple[str, bool]:
    changed = False
    patterns = [
        (r"1[3-9]\d{9}", "[PHONE]"),
        (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[EMAIL]"),
        (r"(微信|WeChat|wechat|VX|vx)[:：]?\s*[A-Za-z0-9_-]{5,}", "[WECHAT]"),
        (r"(QQ|qq)[:：]?\s*\d{5,12}", "[QQ]"),
    ]
    result = text
    for pattern, repl in patterns:
        result, count = re.subn(pattern, repl, result)
        changed = changed or count > 0
    return result, changed


def extract_case(source_name: str, url: str, text: str) -> dict[str, Any]:
    text, pii_changed = redact_inline(text)
    gpa = first_match([
        r"(?:GPA|绩点)[:：\s]*([2-4](?:\.\d+)?\s*/\s*[45](?:\.0)?)",
        r"(?:均分|平均分|成绩)[:：\s]*([6-9]\d(?:\.\d+)?)",
    ], text)
    language = first_match([
        r"((?:IELTS|雅思)[:：\s]*[5-9](?:\.\d)?)",
        r"((?:TOEFL|托福)[:：\s]*\d{2,3})",
    ], text)
    gre_gmat = first_match([
        r"((?:GRE)[:：\s]*\d{3})",
        r"((?:GMAT)[:：\s]*\d{3})",
    ], text)
    year = first_match([r"(20[1-3]\d)[届年]?(?:申请|录取|offer)"], text)
    tier = first_match([r"(C9|985|211|双一流|双非|海本|海外本科)"], text)
    admitted_school = first_match([
        r"(香港大学|香港中文大学|香港科技大学|新加坡国立大学|南洋理工大学|伦敦大学学院|帝国理工学院|伦敦国王学院|曼彻斯特大学|爱丁堡大学)",
        r"((?:University|College|School) of [A-Za-z &.'-]{2,60})",
        r"([A-Za-z &.'-]{2,60} (?:University|College|School))",
    ], text)
    admitted_program = first_match([
        r"((?:MSc|MA|MS|Master of|硕士)[ A-Za-z\u4e00-\u9fff&/-]{2,50}?)(?:offer|录取|。|；|,|，|$)",
        r"((?:金融|商业分析|数据科学|计算机|传媒|教育|管理|会计|经济)[\u4e00-\u9fffA-Za-z &/-]{0,24}(?:硕士|MSc|MA|MS))",
    ], text)
    major = first_match([
        r"(?:本科专业|专业背景)[:：\s]*([\u4e00-\u9fffA-Za-z /&-]{2,24}?)(?:\s|，|,|。|；|GPA|均分|雅思|托福|GRE|GMAT)",
        r"本科(?:专业)?\s*([\u4e00-\u9fffA-Za-z /&-]{2,24}?)(?:\s|，|,|。|；|GPA|均分|雅思|托福|GRE|GMAT)",
    ], text)

    tags = []
    if "香港" in text or "港大" in text or "港中文" in text or "港科技" in text:
        tags.append("hong-kong")
    if "新加坡" in text or "NUS" in text or "NTU" in text:
        tags.append("singapore")
    if "英国" in text or "UCL" in text or "KCL" in text or "曼彻斯特" in text:
        tags.append("uk")
    if "美国" in text:
        tags.append("us")

    confidence = 0.3
    for value in (admitted_school, admitted_program, gpa, language, tier):
        if value:
            confidence += 0.1
    if any(word in text for word in ("实习", "科研", "项目", "竞赛")):
        confidence += 0.1
    confidence = min(confidence, 0.9)
    if confidence < 0.5:
        tags.append("needs_review")

    return {
        "source_name": source_name,
        "source_url": url,
        "crawled_at": now_iso(),
        "case_year": year,
        "target_region": normalize_region(text),
        "admitted_school": admitted_school,
        "admitted_program": admitted_program,
        "undergraduate_school_tier": tier or "unknown",
        "undergraduate_major": major,
        "gpa_text": gpa,
        "gpa_normalized": normalize_gpa(gpa),
        "language_score": language,
        "gre_gmat": gre_gmat,
        "internship_summary": summarize_experience(text, ["实习", "工作经历", "工作经验"]),
        "research_summary": summarize_experience(text, ["科研", "论文", "课题", "研究"]),
        "competition_or_project_summary": summarize_experience(text, ["竞赛", "项目", "比赛"]),
        "result_type": "admit" if any(word in text.lower() for word in ["录取", "offer", "admit", "unconditional"]) else None,
        "tags": sorted(set(tags)),
        "pii_removed": True,
        "extraction_confidence": round(confidence, 2),
    }


def crawl_source(source: dict[str, Any], config: dict[str, Any], seen: set[str]) -> list[dict[str, Any]]:
    user_agent = config.get("user_agent") or DEFAULT_USER_AGENT
    delay = float(config.get("request_delay_seconds", 5))
    max_pages = int(config.get("max_pages_per_source", 20))
    include_keywords = source.get("include_url_keywords", [])
    exclude_keywords = source.get("exclude_url_keywords", [])

    queue = list(source.get("entry_urls", []))
    visited: set[str] = set()
    records: list[dict[str, Any]] = []

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited or url in seen:
            continue
        if any(keyword.lower() in url.lower() for keyword in exclude_keywords):
            continue
        visited.add(url)
        seen.add(url)

        if not can_fetch(url, user_agent):
            continue

        page = fetch(url, user_agent)
        time.sleep(delay)
        if not page:
            continue

        text, links = parse_html(page)
        if looks_blocked(text):
            continue

        for href in links:
            next_url = absolute_url(url, href)
            if not next_url:
                continue
            if urllib.parse.urlparse(next_url).netloc != urllib.parse.urlparse(url).netloc:
                continue
            if any(keyword.lower() in next_url.lower() for keyword in exclude_keywords):
                continue
            if any(keyword.lower() in next_url.lower() for keyword in include_keywords):
                queue.append(next_url)

        if looks_like_case(url, text, include_keywords):
            records.append(extract_case(source.get("name", "unknown"), url, text))

    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Crawl compliant public admissions case pages into JSONL.")
    parser.add_argument("config", help="JSON config path.")
    args = parser.parse_args()

    config = load_config(args.config)
    output = config.get("output_jsonl", "cases.jsonl")
    seen: set[str] = set()

    with open(output, "a", encoding="utf-8") as handle:
        for source in config.get("sources", []):
            for record in crawl_source(source, config, seen):
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
