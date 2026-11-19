#!/usr/bin/env python3
"""
매주 수요일 오전 10:00 KST (01:00 UTC) 주간 글로벌 IT · AI 뉴스 자동 수집기
- 수집 범위: 직전 7일 (when:7d) 주간 핵심 이슈
- 파트 1 (4대 주간 심층 영역):
  01 AI 모델·에이전트, 02 AI 반도체·인프라, 03 빅테크·클라우드·SaaS, 04 피지컬AI·보안·정책
- 파트 2 (주간 IT·AI 주요 단신 8선 Quick Radar):
  01 오픈소스·개발자, 02 스타트업·VC, 03 국내 AI·빅테크, 04 디바이스·온디바이스,
  05 클라우드·데이터, 06 사이버보안, 07 로보틱스·모빌리티, 08 AI 정책·저작권
- 글로벌 1차 테크 RSS(TechCrunch, The Verge, Ars Technica) + Google News KR(when:7d) 병행 수집
- 산출물:
  1) raw_cache/YYYY-MM-DD_AI_Weekly_Cache.json
  2) briefings/YYYY-MM-DD_AI_Weekly_Briefing.md
  3) briefings/YYYY-MM-DD_Slack_Post.txt (Slack 수동 복붙용 3줄 요약 + 4대 헤드라인)
  4) /tmp/latest_ai_issue_body.md (GitHub Issue 알림 본문)
"""
import datetime
import html
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

KST = datetime.timezone(datetime.timedelta(hours=9))
NOW_KST = datetime.datetime.now(KST)
TODAY_STR = NOW_KST.strftime("%Y-%m-%d")
WEEK_START_STR = (NOW_KST - datetime.timedelta(days=7)).strftime("%Y.%m.%d")
TODAY_DOT = NOW_KST.strftime("%Y.%m.%d")
WEEK_RANGE = f"{WEEK_START_STR} ~ {TODAY_DOT}"

# Google Drive 고정 링크 (AI Tech News)
DRIVE_ROOT_URL = "https://drive.google.com/drive/folders/107pVU_TPQS6USbFJsPsf4o_aRBB5TTKc"
DRIVE_WEEKLY_URL = "https://drive.google.com/drive/folders/1wiIpcQGPbBwOqu9t_JxJg2C9LOhQSa60"
DRIVE_VIDEOS_URL = "https://drive.google.com/drive/folders/18gcOJM175VVxb7rgq0wcuU-1u2bISSdI"
MASTER_SLIDE_URL = "https://docs.google.com/presentation/d/1yad5aoY8SAX-fImKETc520AsWWwWwPvWojVLGJTKQ68/edit"

# 4대 주간 심층 영역 (직전 7일 글로벌 + 국내 핵심 이슈)
DEEP_DIVE_DOMAINS = [
    {
        "code": "01",
        "domain": "AI 모델 · 에이전트",
        "region_tag": "실리콘밸리 · 글로벌 AI 랩",
        "kr_query": "(오픈AI OR 앤스로픽 OR 구글 딥마인드 OR 제미나이 OR 클로드 OR AI 에이전트 OR 오픈소스 AI)",
        "en_query": "(OpenAI OR Anthropic OR \"Google DeepMind\" OR \"AI agent\" OR Gemini OR Claude)",
        "slide_page": "3p 심층분석",
    },
    {
        "code": "02",
        "domain": "AI 반도체 · 인프라",
        "region_tag": "미국 · 대만 · 한국",
        "kr_query": "(엔비디아 OR TSMC OR HBM OR AI 반도체 OR SK하이닉스 AI OR 데이터센터 전력)",
        "en_query": "(NVIDIA OR TSMC OR HBM OR \"AI chip\" OR \"data center\" OR Rubin OR Blackwell)",
        "slide_page": "4p 심층분석",
    },
    {
        "code": "03",
        "domain": "빅테크 · 클라우드 · SaaS",
        "region_tag": "북미 빅테크 · 엔터프라이즈",
        "kr_query": "(마이크로소프트 AI OR AWS OR 구글 클라우드 OR 애플 AI OR 메타 AI OR 빅테크 설비투자)",
        "en_query": "(Microsoft Azure OR AWS OR \"Google Cloud\" OR \"Big Tech\" AI OR Apple AI OR Meta AI)",
        "slide_page": "5p 심층분석",
    },
    {
        "code": "04",
        "domain": "피지컬 AI · 보안 · 테크 정책",
        "region_tag": "미국 · 유럽 · 글로벌 규제",
        "kr_query": "(AI 규제 OR AI 안전 OR 사이버보안 AI OR 휴머노이드 로봇 OR 자율주행 AI OR EU AI법)",
        "en_query": "(\"AI regulation\" OR \"AI safety\" OR \"EU AI Act\" OR humanoid robot OR cybersecurity AI)",
        "slide_page": "6p 심층분석",
    },
]

# 주간 IT·AI 주요 단신 브리핑 8선 (Quick Radar)
QUICK_RADAR_CATEGORIES = [
    {"num": "01", "tag": "오픈소스·개발자", "query": "(오픈소스 AI OR 깃허브 코파일럿 OR 허깅페이스 OR 개발자 AI 도구 OR 바이브코딩)"},
    {"num": "02", "tag": "스타트업·VC", "query": "(AI 스타트업 투자 OR AI 유니콘 OR 글로벌 VC AI OR AI 기업가치 OR AI IPO)"},
    {"num": "03", "tag": "국내 AI·빅테크", "query": "(네이버 AI OR 카카오 AI OR 업스테이지 OR 뤼튼 OR SKT AI OR KT AI)"},
    {"num": "04", "tag": "디바이스·온디바이스", "query": "(온디바이스 AI OR AI PC OR AI 스마트폰 OR 갤럭시 AI OR 아이폰 AI OR 스마트글래스)"},
    {"num": "05", "tag": "클라우드·데이터", "query": "(클라우드 장애 OR 데이터센터 투자 OR SaaS AI OR 벡터DB OR 엔터프라이즈 AI)"},
    {"num": "06", "tag": "사이버보안", "query": "(사이버보안 OR 랜섬웨어 OR 해킹 OR AI 보안 위협 OR 제로데이)"},
    {"num": "07", "tag": "로보틱스·모빌리티", "query": "(휴머노이드 OR 피지컬 AI OR 로보택시 OR 테슬라 옵티머스 OR 웨이모)"},
    {"num": "08", "tag": "AI 정책·저작권", "query": "(AI 저작권 OR AI 기본법 OR AI 소송 OR AI 규제 법안 OR AI 워터마크)"},
]

# 글로벌 1차 테크 RSS 보강 피드
GLOBAL_TECH_FEEDS = [
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}


def clean_html(raw_text: str) -> str:
    if not raw_text:
        return ""
    text = html.unescape(raw_text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_google_news_rss(base_query: str, lang: str = "ko", max_items: int = 5):
    hl, gl, ceid = ("ko", "KR", "KR:ko") if lang == "ko" else ("en-US", "US", "US:en")
    for suffix in [" when:7d", " when:14d", ""]:
        query = base_query + suffix
        encoded = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={ceid}"
        req = urllib.request.Request(url, headers=HEADERS)
        items = []
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                xml_bytes = resp.read()
            root = ET.fromstring(xml_bytes)
            for item in root.findall("./channel/item"):
                raw_title = item.findtext("title") or ""
                link = item.findtext("link") or ""
                pub_date = item.findtext("pubDate") or ""
                source_el = item.find("source")
                source_name = source_el.text.strip() if source_el is not None and source_el.text else ("글로벌 테크" if lang == "en" else "IT 종합")

                title = raw_title
                if " - " in raw_title:
                    parts = raw_title.rsplit(" - ", 1)
                    title = parts[0].strip()
                    if source_name in ("IT 종합", "글로벌 테크"):
                        source_name = parts[1].strip()

                pub_kst = ""
                if pub_date:
                    try:
                        dt = parsedate_to_datetime(pub_date).astimezone(KST)
                        pub_kst = dt.strftime("%m/%d %H:%M")
                    except Exception:
                        pub_kst = pub_date[:16]

                items.append(
                    {
                        "title": clean_html(title),
                        "source": source_name,
                        "link": link,
                        "pub_kst": pub_kst,
                        "lang": lang,
                    }
                )
                if len(items) >= max_items:
                    break
        except Exception as exc:
            print(f"[WARN] Google News RSS failed for '{query}' ({lang}): {exc}")

        if items:
            return items
    return []


def fetch_global_tech_feeds(max_per_feed: int = 4):
    collected = []
    for feed_name, url in GLOBAL_TECH_FEEDS:
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml_bytes = resp.read()
            root = ET.fromstring(xml_bytes)
            # Support both RSS <item> and Atom <entry>
            entries = root.findall("./channel/item")
            is_atom = False
            if not entries:
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                entries = root.findall("atom:entry", ns)
                is_atom = True

            count = 0
            for el in entries:
                if is_atom:
                    ns = {"atom": "http://www.w3.org/2005/Atom"}
                    title = clean_html(el.findtext("atom:title", "", ns))
                    link_el = el.find("atom:link", ns)
                    link = link_el.attrib.get("href", "") if link_el is not None else ""
                    pub = el.findtext("atom:updated", "", ns)[:10]
                else:
                    title = clean_html(el.findtext("title") or "")
                    link = el.findtext("link") or ""
                    pub_raw = el.findtext("pubDate") or ""
                    try:
                        pub = parsedate_to_datetime(pub_raw).astimezone(KST).strftime("%m/%d %H:%M")
                    except Exception:
                        pub = pub_raw[:16]

                if title and link:
                    collected.append(
                        {"title": title, "source": feed_name, "link": link, "pub_kst": pub, "lang": "en"}
                    )
                    count += 1
                if count >= max_per_feed:
                    break
        except Exception as exc:
            print(f"[WARN] Direct feed '{feed_name}' failed: {exc}")
    return collected


def collect_all():
    seen_titles = set()
    deep_dive_results = []
    for d in DEEP_DIVE_DOMAINS:
        kr_items = fetch_google_news_rss(d["kr_query"], lang="ko", max_items=5)
        en_items = fetch_google_news_rss(d["en_query"], lang="en", max_items=4)
        combined = kr_items[:3] + en_items[:2]
        deduped = []
        for art in combined:
            key = art["title"][:22].lower()
            if key not in seen_titles:
                seen_titles.add(key)
                deduped.append(art)
            if len(deduped) >= 4:
                break
        deep_dive_results.append({**d, "articles": deduped})

    radar_results = []
    for r in QUICK_RADAR_CATEGORIES:
        fetched = fetch_google_news_rss(r["query"], lang="ko", max_items=5)
        chosen = None
        for art in fetched:
            key = art["title"][:22].lower()
            if key not in seen_titles:
                seen_titles.add(key)
                chosen = art
                break
        if not chosen and fetched:
            chosen = fetched[0]
        radar_results.append({**r, "article": chosen})

    global_highlights = fetch_global_tech_feeds(max_per_feed=4)

    return {
        "date": TODAY_STR,
        "week_range": WEEK_RANGE,
        "generated_at_kst": NOW_KST.strftime("%Y-%m-%d %H:%M:%S KST"),
        "deep_dives": deep_dive_results,
        "quick_radar": radar_results,
        "global_tech_feeds": global_highlights,
    }


def render_slack_post(data: dict) -> str:
    lines = []
    lines.append(f"🤖 *[주간 IT · AI 핵심 브리핑]* ({data['week_range']})")
    lines.append("이번 주 글로벌·국내 IT·AI 핵심 4대 이슈를 3분 영상으로 정리했습니다. 🎬")
    lines.append("")
    lines.append("*📌 이번 주 4대 핵심 이슈*")
    for d in data["deep_dives"]:
        articles = d.get("articles", [])
        if articles:
            lead = articles[0]
            lines.append(f"• *[{d['domain']}]* {lead['title']} ({lead['source']})")
        else:
            lines.append(f"• *[{d['domain']}]* 주간 핵심 이슈 집계 중")
    lines.append("")
    lines.append("*⚡ 주간 단신 레이더 TOP 4*")
    for r in data["quick_radar"][:4]:
        art = r.get("article")
        if art:
            lines.append(f"• `{r['tag']}` {art['title']}")
    lines.append("")
    lines.append(f"📊 슬라이드 원본: {MASTER_SLIDE_URL}")
    lines.append(f"📁 주간 브리핑 아카이브: {DRIVE_WEEKLY_URL}")
    return "\n".join(lines)


def render_markdown(data: dict, slack_text: str) -> str:
    lines = []
    lines.append(f"# 🤖 [{data['week_range']}] 주간 IT · AI 핵심 이슈 리포트 (4대 심층분석 + 단신 8선)")
    lines.append("")
    lines.append(f"> **자동 수집 시각**: `{data['generated_at_kst']}` (매주 수요일 10:00 KST)  |  **수신**: `@starjw2010-cloud`")
    lines.append(">")
    lines.append(f"> - 📊 **[8장 영상용 마스터 슬라이드 열기 (Google Slides)]({MASTER_SLIDE_URL})**")
    lines.append(f"> - 📁 **[AI Tech News 드라이브 폴더]({DRIVE_ROOT_URL})**")
    lines.append(f"> - 🗂️ **[02_Weekly_Briefings (주간 슬라이드·PDF)]({DRIVE_WEEKLY_URL})**")
    lines.append(f"> - 🎬 **[03_Weekly_Videos (아바타·자막 MP4)]({DRIVE_VIDEOS_URL})**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🧠 파트 1. 주간 IT · AI 4대 핵심 영역 심층 스캔 (직전 7일)")
    lines.append("")

    for d in data["deep_dives"]:
        lines.append(f"### {d['code']}. [{d['domain']}] ({d['region_tag']} · {d['slide_page']})")
        articles = d.get("articles", [])
        if not articles:
            lines.append("- 이번 주 신규 주요 기사가 수집되지 않았습니다.")
        else:
            lead = articles[0]
            lines.append(f"- **핵심 헤드라인**: **[{lead['title']}]({lead['link']})** (`{lead['source']}`, {lead['pub_kst']})")
            if len(articles) > 1:
                lines.append("- **연관 교차검증 기사 (글로벌·국내)**:")
                for sub in articles[1:]:
                    lang_badge = "🌐" if sub.get("lang") == "en" else "🇰🇷"
                    lines.append(f"  - {lang_badge} [{sub['title']}]({sub['link']}) (`{sub['source']}`, {sub['pub_kst']})")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## ⚡ 파트 2. 주간 IT · AI 주요 단신 8선 (Quick Radar)")
    lines.append("")
    lines.append("| 번호 | 분야 | 핵심 단신 헤드라인 (원문 링크) | 출처 · 시각 |")
    lines.append("| :---: | :---: | :--- | :---: |")
    for r in data["quick_radar"]:
        art = r.get("article")
        if art:
            lines.append(f"| **{r['num']}** | `{r['tag']}` | **[{art['title']}]({art['link']})** | `{art['source']}` ({art['pub_kst']}) |")
        else:
            lines.append(f"| **{r['num']}** | `{r['tag']}` | 신규 단신 집계 중 | - |")

    if data.get("global_tech_feeds"):
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 🌐 파트 3. 글로벌 1차 테크 미디어 헤드라인 (TechCrunch · The Verge · Ars Technica)")
        lines.append("")
        for g in data["global_tech_feeds"][:8]:
            lines.append(f"- **[{g['source']}]** [{g['title']}]({g['link']}) ({g['pub_kst']})")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 💬 Slack 복붙용 포스팅 초안")
    lines.append("")
    lines.append("```text")
    lines.append(slack_text)
    lines.append("```")
    lines.append("")
    lines.append("## 🎬 영상 제작 & Slack 발행 가이드 (3분 컷)")
    lines.append("1. **Antigravity** 채팅창에 **`\"이번 주 IT·AI 브리핑 슬라이드 만들어줘\"`** 입력 → 우측 하단 아바타 PiP · 하단 자막 Safe Zone이 반영된 **8장 Google Slides + 방송 대본(발표자 노트)** 자동 생성")
    lines.append("2. Google Slides에서 **`파일 → 동영상으로 변환 (Google Vids)`** 클릭 → **`발표자 노트로 대체`** 선택")
    lines.append("3. 8장 전 슬라이드 우측 하단에 **한국어 AI 아바타** 배치 + 우측 사이드바 **`Captions(스타일 자막)`** 전체 적용 → **MP4 다운로드**")
    lines.append("4. MP4 + 위 Slack 복붙 텍스트를 Slack 채널에 업로드 완료!")
    lines.append("")
    return "\n".join(lines)


def main():
    os.makedirs("raw_cache", exist_ok=True)
    os.makedirs("briefings", exist_ok=True)

    data = collect_all()
    raw_path = os.path.join("raw_cache", f"{TODAY_STR}_AI_Weekly_Cache.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    slack_text = render_slack_post(data)
    slack_path = os.path.join("briefings", f"{TODAY_STR}_Slack_Post.txt")
    with open(slack_path, "w", encoding="utf-8") as f:
        f.write(slack_text + "\n")

    md_content = render_markdown(data, slack_text)
    md_path = os.path.join("briefings", f"{TODAY_STR}_AI_Weekly_Briefing.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    with open("/tmp/latest_ai_issue_body.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[OK] Saved {raw_path}, {md_path}, {slack_path}")


if __name__ == "__main__":
    main()
