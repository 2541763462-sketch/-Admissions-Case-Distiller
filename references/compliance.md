# Compliance Reference

## Operating Principle

Public visibility does not automatically grant permission for unrestricted collection, storage, redistribution, or model training. This skill treats public pages as sources for limited factual extraction and aggregate analysis only.

## Allowed Collection

Collect only when all conditions are true:
- The page is reachable without login, payment, captcha, or special session state.
- robots.txt allows fetching for the configured user agent.
- The crawler uses low frequency and stops on repeated errors.
- The page is relevant to admissions cases or official program requirements.
- Stored data is anonymous, structured, and traceable to a source URL.

## Must Skip

Skip pages with:
- Login prompts, member-center routes, paywall prompts, captcha pages, or "access denied" notices.
- Explicit no-crawl terms in robots.txt.
- Full student essays, full CVs, contact details, avatars, or identity-heavy profiles.
- Content that appears copied from private consultation systems or closed communities.

## Storage Rules

Store:
- Source name and URL
- Crawl timestamp
- Anonymous background fields
- Brief non-verbatim summaries
- Extraction confidence
- Review tags

Do not store:
- Full HTML
- Full article bodies
- Student names
- Photos or avatars
- Phone, email, WeChat, QQ, student IDs
- Complete essays or CVs
- Highly specific stories that can identify a person

## Crawl Conduct

Use:
- Clear user agent
- Configurable rate limit, default 5 seconds or slower
- Max page count per source
- robots.txt check
- Retry limits

Do not use:
- Cookie replay
- Login automation
- Captcha solving
- Proxy rotation to evade controls
- Header spoofing intended to bypass blocking
- Hidden API reverse engineering when the page is not normally accessible

## Output Language

Prefer:
- "public-case index"
- "anonymous admissions-pattern analysis"
- "公开案例洞察"

Avoid:
- "secret scraping"
- "stealth crawler"
- "copy case library"
- "essay washing"
