# 🤖 Weekly IT & AI Briefing Bot (`ai-tech-weekly-briefing`)

매주 **수요일 오전 10시(한국시간 KST 기준, `0 1 * * 3` UTC)** 에 직전 7일간의 글로벌·국내 IT·AI 핵심 뉴스를 자동 스캔하여 **주간 4대 심층 영역 + 주요 단신 8선(총 12건)** 을 수집·아카이빙하고, **Google Slides(우측 하단 아바타 PiP · 하단 자막 Safe Zone + 방송 대본 Speaker Notes)** → **Google Vids AI 아바타 영상** → **Slack 공유**까지 연결하는 주간 IT·AI 뉴스룸 파이프라인입니다.

---

## 🔗 구글 드라이브 마스터 리소스 (`AI Tech News`)
- 📁 **[AI Tech News 루트 폴더](https://drive.google.com/drive/folders/107pVU_TPQS6USbFJsPsf4o_aRBB5TTKc)**
- 📚 **[00_Instructions (지침서 · 마스터 템플릿 · 에셋)](https://drive.google.com/drive/folders/1LntPPOx865ue7KIpRAlHDbMWZlrwoCVa)**
- 📊 **[[Template] AI_Tech_Weekly_Briefing_Video_Deck (영상용 8장 마스터 슬라이드)](https://docs.google.com/presentation/d/1yad5aoY8SAX-fImKETc520AsWWwWwPvWojVLGJTKQ68/edit)**
- 🗂️ **[02_Weekly_Briefings (주간 슬라이드 · PDF 아카이브)](https://drive.google.com/drive/folders/1wiIpcQGPbBwOqu9t_JxJg2C9LOhQSa60)**
- 🎬 **[03_Weekly_Videos (Google Vids 아바타 · 자막 MP4 보관함)](https://drive.google.com/drive/folders/18gcOJM175VVxb7rgq0wcuU-1u2bISSdI)**

---

## ⏰ 자동 작동 방식 (매주 수요일 오전 10:00 KST)
1. **직전 7일 글로벌·국내 IT·AI 뉴스 자동 수집 ([`scripts/collect_weekly_ai_news.py`](scripts/collect_weekly_ai_news.py))**
   - **파트 1 (4대 주간 심층 영역)**: `01 AI 모델·에이전트`, `02 AI 반도체·인프라`, `03 빅테크·클라우드·SaaS`, `04 피지컬 AI·보안·테크 정책`
   - **파트 2 (주간 단신 8선 레이더)**: `오픈소스·개발자`, `스타트업·VC`, `국내 AI·빅테크`, `디바이스·온디바이스`, `클라우드·데이터`, `사이버보안`, `로보틱스·모빌리티`, `AI 정책·저작권`
   - **파트 3 (글로벌 1차 테크 피드)**: TechCrunch AI, The Verge AI, Ars Technica 병행 수집
2. **원문 캐시 · 마크다운 리포트 · Slack 복붙 텍스트 자동 저장**
   - `raw_cache/YYYY-MM-DD_AI_Weekly_Cache.json`
   - `briefings/YYYY-MM-DD_AI_Weekly_Briefing.md`
   - `briefings/YYYY-MM-DD_Slack_Post.txt`
3. **GitHub Issue 자동 발행 → 이메일 알림 발송**
   - 매주 수요일 오전 10시 새 Issue(`🤖 [주간 IT·AI 브리핑] YYYY.MM.DD 4대 핵심 이슈 & 주요 단신 8선`)가 생성됩니다.

---

## 🎬 원할 때마다 3분 만에 아바타·자막 영상 제작 → Slack 퍼블리싱
1. **1차 제작 (Antigravity)**: 채팅창에 **`"이번 주 IT·AI 브리핑 슬라이드 만들어줘"`** 입력
   - 8장 전 슬라이드 **우측 하단 아바타(PiP) 전용 존(`x ≥ 560pt, y ≥ 256pt`)** + **하단 자막 Safe Zone(`y ≥ 338pt`)** 완벽 반영
   - 슬라이드별 25~35초 한국어 아나운서 방송 대본(`Speaker Notes`) 자동 주입 (총 약 3분 50초)
   - 9개 정량 도표 + 글로벌 AI 거점 지도 + Slack 복붙용 요약문 생성
2. **2차 영상화 (Google Slides → Google Vids, AI Ultra)**:
   - 생성된 Google Slides에서 **`파일 → 동영상으로 변환(Convert to Video)`** 클릭
   - **`발표자 노트로 대체(Replace with speaker notes)`** 선택하여 방송 대본 즉시 로드
   - 8장 전 슬라이드 우측 하단 빈 공간에 **한국어 AI 아바타(PiP)** 배치
   - 우측 사이드바 **`Captions`** 에서 **스타일 자막(오픈 캡션)** 전체 적용 후 IT 고유명사만 빠르게 검수 → **MP4 다운로드** (`03_Weekly_Videos` 보관)
3. **3차 발행 (Slack 수동 업로드)**:
   - MP4 영상 파일 + `briefings/YYYY-MM-DD_Slack_Post.txt` 복붙으로 10초 만에 발행 완료!
