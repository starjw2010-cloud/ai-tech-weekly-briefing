#!/usr/bin/env python3
"""
주간 IT · AI 영상용 8장 마스터 슬라이드 빌더 (Google Slides → Google Vids 최적화 표준 v1.0)
- 모든 슬라이드(1~8p) 공통 영상 Safe Zone 엄수:
  1) 우측 하단 AI 아바타(PiP) 전용 존: x >= 560pt, y >= 256pt (160x149pt 완전 공백)
  2) 하단 자막(Styled Captions) 안전 영역: y >= 338pt (하단 67pt 완전 공백)
- 모든 슬라이드(1~8p) Speaker Notes에 25~35초 한국어 방송 아나운서 대본 자동 주입
  (Google Vids [파일 → 동영상으로 변환] → [발표자 노트로 대체] 원클릭 연동)
- 순수 한국어 에디토리얼 표준 + 9개 정량 도표 + PDF 내보내기 자동 검증 지원
"""
import json
import os
import subprocess
import sys

PRES_ID = os.environ.get("AI_DECK_PRES_ID", "1yad5aoY8SAX-fImKETc520AsWWwWwPvWojVLGJTKQ68")
COVER_URL = os.environ.get("AI_COVER_URL", "https://drive.google.com/uc?export=download&id=1Klia_afsKagU4wSxrnB9PKfqjWdi1heQ")
MAP_URL = os.environ.get("AI_MAP_URL", "https://drive.google.com/uc?export=download&id=1cy9VQLF-XE19Ucz3rvMGIjBQMEFAWpop")
PDF_OUT_PATH = os.environ.get("AI_PDF_OUT", "/tmp/Sample_AI_Tech_Weekly_Briefing.pdf")

true = True
false = False


def build_deck():
    raw = subprocess.check_output(["gslides", "readonly", "list-slides", PRES_ID, "--json"], text=True)
    slides = json.loads(raw)
    s1_id = slides[0]["objectId"]
    slide1_elements = [pe["objectId"] for pe in slides[0].get("pageElements", [])]
    other_slides = [s["objectId"] for s in slides[1:]]

    for sid in other_slides:
        subprocess.run(["gslides", "mutate", "delete-slide", PRES_ID, sid], check=True)

    ops = [{"op": "delete-element", "element": eid} for eid in slide1_elements]

    ops.extend([
        # =====================================================================
        # SLIDE 1: 표지 (우측 상단 일러스트 / 우측 하단 아바타 PiP 존 · 하단 자막 존 확보)
        # =====================================================================
        {"op": "set-background", "slide": s1_id, "color": "#FFFFFF"},
        {"op": "add-textbox", "slide": s1_id, "text": "주간 글로벌 IT · AI 심층 브리핑  (영상용 마스터)", "x": 48, "y": 58, "width": 340, "height": 20, "font_size": 10.5, "bold": true, "color": "#0284C7", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": s1_id, "text": "주간 IT · AI\n핵심 이슈 리포트", "x": 48, "y": 84, "width": 340, "height": 96, "font_size": 34, "bold": true, "color": "#0F172A", "font_family": "Roboto", "line_spacing": 122},
        {"op": "add-shape", "slide": s1_id, "shape_type": "RECTANGLE", "x": 48, "y": 192, "width": 52, "height": 3, "background_color": "#1E3A8A"},
        {"op": "add-textbox", "slide": s1_id, "text": "01 AI 모델 · 에이전트    |    02 AI 반도체 · 인프라\n03 빅테크 · 클라우드     |    04 피지컬 AI · 보안 · 정책", "x": 48, "y": 210, "width": 345, "height": 46, "font_size": 11, "bold": true, "color": "#475569", "font_family": "Roboto", "line_spacing": 155},
        {"op": "add-textbox", "slide": s1_id, "text": "2026. 11. 12 ~ 11. 19   ·   주간 4대 심층분석 + IT 단신 8선", "x": 48, "y": 274, "width": 350, "height": 22, "font_size": 10, "color": "#64748B", "font_family": "Roboto"},
        {"op": "add-shape", "slide": s1_id, "shape_type": "ROUND_RECTANGLE", "x": 48, "y": 302, "width": 295, "height": 24, "background_color": "#EFF6FF"},
        {"op": "add-textbox", "slide": s1_id, "text": "매주 수요일 오전 10시 발행  ·  3분 브리핑 영상 최적화본", "x": 56, "y": 304, "width": 280, "height": 20, "font_size": 8.8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-image", "slide": s1_id, "url": COVER_URL, "x": 426, "y": 22, "width": 212, "height": 228},
        {"op": "set-notes", "slide": s1_id, "text": "안녕하세요, 주간 글로벌 IT·AI 핵심 이슈 브리핑입니다. 십일월 둘째 주와 셋째 주 사이, 글로벌 인공지능 산업을 뒤흔든 네 가지 핵심 이슈와 놓치면 안 될 주요 단신 여덟 건을 삼 분 만에 핵심만 짚어드리겠습니다."},

        # =====================================================================
        # SLIDE 2: 주간 IT·AI 요약 & 글로벌 AI 거점 지도
        # 좌측(x=45..365): 4대 이슈 요약 / 우상단(x=380..675, y=82..248): 세계지도
        # 우하단(x=560..720, y=256..405) & 하단(y=338..405): 아바타·자막 Safe Zone
        # =====================================================================
        {"op": "add-slide", "layout": "BLANK", "id": "S_SUMMARY"},
        {"op": "set-background", "slide": "S_SUMMARY", "color": "#FFFFFF"},
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "주간 IT · AI 핵심 요약  (2 / 8)", "x": 45, "y": 18, "width": 400, "height": 16, "font_size": 10, "bold": true, "color": "#0284C7", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "글로벌 AI · 반도체 거점별 주간 4대 핵심 이슈", "x": 45, "y": 35, "width": 630, "height": 28, "font_size": 20, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_SUMMARY", "shape_type": "RECTANGLE", "x": 45, "y": 70, "width": 630, "height": 1.5, "background_color": "#0F172A"},

        # Left Column: 4 Core Weekly Issues (x=45..365, y=78..330)
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "01  AI 모델 · 앤스로픽 나스닥 상장 & 매출 800억$  (→ 3p)", "x": 45, "y": 78, "width": 320, "height": 18, "font_size": 10, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "앤스로픽 11/19 나스닥(ANT) 상장, 연환산 매출 800억 달러 돌파\n오픈AI와 기업용 AI 매출 패권 경쟁 격화  (가디언 · 외신종합)", "x": 45, "y": 96, "width": 320, "height": 34, "font_size": 9.2, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "add-shape", "slide": "S_SUMMARY", "shape_type": "RECTANGLE", "x": 45, "y": 135, "width": 318, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "02  AI 반도체 · 엔비디아 3Q 매출 1,158억$ 돌파  (→ 4p)", "x": 45, "y": 141, "width": 320, "height": 18, "font_size": 10, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "전년비 111% 성장 및 차세대 베라 루빈 출하 본격화로 우려 불식\n대만 TSMC 패키징·국내 HBM 수요 재확인  (엔비디아 실적발표)", "x": 45, "y": 159, "width": 320, "height": 34, "font_size": 9.2, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "add-shape", "slide": "S_SUMMARY", "shape_type": "RECTANGLE", "x": 45, "y": 198, "width": 318, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "03  클라우드 · 미국 IT 인프라 6일간 7건 연쇄 장애  (→ 5p)", "x": 45, "y": 204, "width": 320, "height": 18, "font_size": 10, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "MS 365·AWS 동부·애플·항공·은행까지 6일 연속 서비스 중단\n연 7,200억 달러 데이터센터 투자 속 안정성 리스크 부각  (테크리퍼블릭)", "x": 45, "y": 222, "width": 320, "height": 34, "font_size": 9.2, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "add-shape", "slide": "S_SUMMARY", "shape_type": "RECTANGLE", "x": 45, "y": 261, "width": 318, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "04  정책·보안 · 오픈AI 안전심사 & 캘리포니아 SB 813  (→ 6p)", "x": 45, "y": 267, "width": 320, "height": 18, "font_size": 10, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "오픈AI 출시 전 4단계 안전심사 의무화, 캘리포니아 독립검증 가동\n유로폴 14개국 합동 작전으로 악성 서버 235대 압수  (주정부·유로폴)", "x": 45, "y": 285, "width": 320, "height": 34, "font_size": 9.2, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},

        # Right-Top Map Frame (x=378..675, y=78..248 -> ends strictly above Avatar PiP y=256)
        {"op": "add-shape", "slide": "S_SUMMARY", "shape_type": "ROUND_RECTANGLE", "x": 378, "y": 78, "width": 297, "height": 170, "background_color": "#F8FAFC"},
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "글로벌 AI · 반도체 이슈 거점 및 파급 경로", "x": 388, "y": 82, "width": 275, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-image", "slide": "S_SUMMARY", "url": MAP_URL, "x": 384, "y": 100, "width": 285, "height": 142},
        # Map legend cleanly in x=378..548, y=256..328 (left of Avatar PiP x=560)
        {"op": "add-shape", "slide": "S_SUMMARY", "shape_type": "ROUND_RECTANGLE", "x": 378, "y": 256, "width": 170, "height": 70, "background_color": "#F8FAFC"},
        {"op": "add-textbox", "slide": "S_SUMMARY", "text": "지도 범례\n■ 인디고·시안: 글로벌 AI 발원지\n■ 레드: 한국 HBM·IT 파급\n┄ 점선: 공급망·규제 전이 경로", "x": 386, "y": 261, "width": 156, "height": 60, "font_size": 7.8, "color": "#475569", "font_family": "Roboto", "line_spacing": 140},
        {"op": "set-notes", "slide": "S_SUMMARY", "text": "이번 주 글로벌 테크 지도를 보면 네 개의 큰 축이 뚜렷합니다. 첫째, 실리콘밸리에서 앤스로픽이 나스닥 상장에 나서며 매출 팔백억 달러 시대를 열었습니다. 둘째, 엔비디아가 분기 매출 천백오십팔억 달러로 반도체 우려를 단숨에 잠재웠고요. 셋째, 미국 핵심 클라우드와 항공망에서 연쇄 장애가 터졌고, 넷째, 미국과 유럽의 인공지능 안전 규제가 본격화됐습니다."},

        # =====================================================================
        # SLIDE 3: 심층 분석 01 · AI 모델 및 에이전트
        # Left Panel (x=45..295, y=94..316): 도표 1 & 도표 2
        # Right Panel: 01(y=96..162, w=363), 02(y=170..236, w=363), 03(y=246..316, w=236 -> ends x=548!)
        # Bottom source: y=320..334, x=45..548
        # =====================================================================
        {"op": "add-slide", "layout": "BLANK", "id": "S_DEEP_MODEL"},
        {"op": "set-background", "slide": "S_DEEP_MODEL", "color": "#FFFFFF"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "심층 분석 01  ·  AI 모델 · 에이전트  (3 / 8)", "x": 45, "y": 16, "width": 400, "height": 16, "font_size": 10, "bold": true, "color": "#0284C7", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "앤스로픽 나스닥 상장 개시, 기업용 AI 매출 패권 격돌", "x": 45, "y": 33, "width": 630, "height": 28, "font_size": 20, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "연환산 매출 800억 달러 돌파하며 상장 선점… 오픈AI는 1.25조 달러 민간 조달로 맞불", "x": 45, "y": 63, "width": 630, "height": 18, "font_size": 11, "color": "#475569", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 45, "y": 86, "width": 630, "height": 1.5, "background_color": "#0F172A"},

        # Left Panel Charts (x=45..295, y=94..316)
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "ROUND_RECTANGLE", "x": 45, "y": 94, "width": 250, "height": 222, "background_color": "#F8FAFC"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "도표 1. AI 선도 2사 연환산 매출 비교 (억 달러)", "x": 54, "y": 100, "width": 232, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},

        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "앤스로픽 10월", "x": 50, "y": 120, "width": 70, "height": 15, "font_size": 7.8, "bold": true, "color": "#0F172A", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 122, "y": 122, "width": 116, "height": 10, "background_color": "#1E3A8A"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "800억$", "x": 244, "y": 120, "width": 44, "height": 15, "font_size": 8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "오픈AI 연말", "x": 50, "y": 140, "width": 70, "height": 15, "font_size": 7.8, "bold": true, "color": "#0F172A", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 122, "y": 142, "width": 101, "height": 10, "background_color": "#0284C7"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "700억$", "x": 229, "y": 140, "width": 44, "height": 15, "font_size": 8, "bold": true, "color": "#0284C7", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "오픈AI 9월", "x": 50, "y": 160, "width": 70, "height": 15, "font_size": 7.8, "color": "#475569", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 122, "y": 162, "width": 72, "height": 10, "background_color": "#94A3B8"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "500억$", "x": 200, "y": 160, "width": 44, "height": 15, "font_size": 7.8, "color": "#64748B", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 54, "y": 182, "width": 232, "height": 1, "background_color": "#E2E8F0"},

        # Chart 2: Vertical Bar
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "도표 2. 앤스로픽 2026년 매출 급성장 (억 달러)", "x": 54, "y": 188, "width": 232, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 54, "y": 207, "width": 232, "height": 100, "background_color": "#FFFFFF"},
        {"op": "add-line", "slide": "S_DEEP_MODEL", "x": 64, "y": 284, "width": 212, "height": 0, "color": "#94A3B8", "line_weight": 1},

        # Bar 1: 1~2Q 합산 162억 (h=24 -> y=260..284, label y=240..255)
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "162억$", "x": 66, "y": 240, "width": 48, "height": 15, "font_size": 7.8, "color": "#64748B", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 75, "y": 260, "width": 30, "height": 24, "background_color": "#CBD5E1"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "상반기(1~2Q)", "x": 60, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "color": "#64748B", "font_family": "Roboto", "alignment": "center"},

        # Bar 2: 3Q 단독 170억 (h=26 -> y=258..284, label y=238..253)
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "170억$", "x": 144, "y": 238, "width": 48, "height": 15, "font_size": 7.8, "bold": true, "color": "#0284C7", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 153, "y": 258, "width": 30, "height": 26, "background_color": "#0284C7"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "3분기 단독", "x": 138, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "bold": true, "color": "#475569", "font_family": "Roboto", "alignment": "center"},

        # Bar 3: 1~3Q 누적 332억 (h=50 -> y=234..284, label y=214..229)
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "332억$", "x": 220, "y": 214, "width": 48, "height": 15, "font_size": 8.2, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 229, "y": 234, "width": 30, "height": 50, "background_color": "#1E3A8A"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "1~3Q 누적", "x": 214, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "bold": true, "color": "#0F172A", "font_family": "Roboto", "alignment": "center"},

        # Right Panel 3-Layer Analysis (Layer 03 strictly ends at x=548 for Avatar PiP!)
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "01  기술 · 시장 배경", "x": 312, "y": 96, "width": 363, "height": 18, "font_size": 11, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "앤스로픽이 공모가 70~78달러로 11월 19일 나스닥(ANT) 상장을 개시하며\n3분기 단독 170억 달러 매출을 증명, 기업용 AI 수익화 원년을 공식화", "x": 312, "y": 116, "width": 363, "height": 40, "font_size": 9.5, "color": "#334155", "font_family": "Roboto", "line_spacing": 140},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 312, "y": 162, "width": 363, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "02  수혜 및 타격 플레이어", "x": 312, "y": 170, "width": 363, "height": 18, "font_size": 11, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "수혜: 클라우드 파트너(AWS·구글) 및 코딩·업무 에이전트 도입 기업\n부담: 수익 모델 검증 압박을 받는 중소 파운데이션 모델·래퍼 스타트업", "x": 312, "y": 190, "width": 363, "height": 40, "font_size": 9.5, "color": "#334155", "font_family": "Roboto", "line_spacing": 140},
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "RECTANGLE", "x": 312, "y": 236, "width": 236, "height": 1, "background_color": "#E2E8F0"},

        # Layer 03 Compact Highlight Card (x=312..548, y=244..316 -> Safe from PiP x=560 & Subtitle y=338)
        {"op": "add-shape", "slide": "S_DEEP_MODEL", "shape_type": "ROUND_RECTANGLE", "x": 312, "y": 244, "width": 236, "height": 72, "background_color": "#EFF6FF"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "03  국내 IT · 비즈니스 시사점", "x": 320, "y": 249, "width": 220, "height": 16, "font_size": 10, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "AI 시장 평가 기준이 '기술력'에서 '매출·ROI'로\n완전 이동. 사내 도입 시 코딩·문서 자동화 등\n정량 성과가 검증된 에이전트 우선 적용 필수", "x": 320, "y": 267, "width": 220, "height": 46, "font_size": 8.8, "bold": true, "color": "#0F172A", "font_family": "Roboto", "line_spacing": 135},

        {"op": "add-textbox", "slide": "S_DEEP_MODEL", "text": "팩트체크 근거: 앤스로픽 상장 공시·가디언·외신 매출 집계 교차검증 완료", "x": 45, "y": 320, "width": 500, "height": 15, "font_size": 8.2, "color": "#64748B", "font_family": "Roboto"},
        {"op": "set-notes", "slide": "S_DEEP_MODEL", "text": "첫 번째 심층 이슈는 인공지능 모델 패권전입니다. 앤스로픽이 십일월 십구일 나스닥 상장을 개시하며, 삼분기 단독 백칠십억 달러, 연환산 팔백억 달러 매출을 돌파했습니다. 오픈에이아이 역시 일조 이천오백억 달러 가치로 민간 자금을 유치하며 맞불을 놓았는데요. 이제 기업 현장의 인공지능 도입도 신기한 기술 체험을 넘어, 코딩과 업무 자동화에서 확실한 투자 대비 성과를 뽑는 단계로 완전히 넘어갔습니다."},

        # =====================================================================
        # SLIDE 4: 심층 분석 02 · AI 반도체 및 인프라
        # =====================================================================
        {"op": "add-slide", "layout": "BLANK", "id": "S_DEEP_CHIP"},
        {"op": "set-background", "slide": "S_DEEP_CHIP", "color": "#FFFFFF"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "심층 분석 02  ·  AI 반도체 · 인프라  (4 / 8)", "x": 45, "y": 16, "width": 400, "height": 16, "font_size": 10, "bold": true, "color": "#0284C7", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "엔비디아 3분기 매출 1,158억 달러 서프라이즈, 베라 루빈 출격", "x": 45, "y": 33, "width": 630, "height": 28, "font_size": 20, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "데이터센터 매출 1,076억 달러(+110% YoY)·총이익률 74.9%… 아시아 반도체 경계감 해소", "x": 45, "y": 63, "width": 630, "height": 18, "font_size": 11, "color": "#475569", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 45, "y": 86, "width": 630, "height": 1.5, "background_color": "#0F172A"},

        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "ROUND_RECTANGLE", "x": 45, "y": 94, "width": 250, "height": 222, "background_color": "#F8FAFC"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "도표 3. 엔비디아 FY27 3Q 실적 vs 전망 (억 달러)", "x": 54, "y": 100, "width": 232, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},

        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "실제 총매출", "x": 52, "y": 120, "width": 64, "height": 15, "font_size": 7.8, "bold": true, "color": "#0F172A", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 118, "y": 122, "width": 114, "height": 10, "background_color": "#1E3A8A"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "1,158억$", "x": 238, "y": 120, "width": 52, "height": 15, "font_size": 7.8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "월가 컨센서스", "x": 52, "y": 140, "width": 64, "height": 15, "font_size": 7.8, "color": "#475569", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 118, "y": 142, "width": 106, "height": 10, "background_color": "#94A3B8"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "1,088억$", "x": 230, "y": 140, "width": 52, "height": 15, "font_size": 7.8, "color": "#64748B", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "데이터센터", "x": 52, "y": 160, "width": 64, "height": 15, "font_size": 7.8, "bold": true, "color": "#0284C7", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 118, "y": 162, "width": 104, "height": 10, "background_color": "#0284C7"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "1,076억$", "x": 228, "y": 160, "width": 52, "height": 15, "font_size": 7.8, "bold": true, "color": "#0284C7", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 54, "y": 182, "width": 232, "height": 1, "background_color": "#E2E8F0"},

        # Chart 4: Pre-earnings Asian chip dip (%)
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "도표 4. 실적 직전 아시아 AI 반도체 조정폭 (%)", "x": 54, "y": 188, "width": 232, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 54, "y": 207, "width": 232, "height": 100, "background_color": "#FFFFFF"},
        {"op": "add-line", "slide": "S_DEEP_CHIP", "x": 64, "y": 284, "width": 212, "height": 0, "color": "#94A3B8", "line_weight": 1},

        # SK Hynix -7.9% (h=48 -> y=236..284, label y=216..231)
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "-7.9%", "x": 66, "y": 216, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#DC2626", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 75, "y": 236, "width": 30, "height": 48, "background_color": "#DC2626"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "SK하이닉스", "x": 60, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "bold": true, "color": "#0F172A", "font_family": "Roboto", "alignment": "center"},

        # TSMC -5.7% (h=35 -> y=249..284, label y=229..244)
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "-5.7%", "x": 144, "y": 229, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#475569", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 153, "y": 249, "width": 30, "height": 35, "background_color": "#64748B"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "대만 TSMC", "x": 138, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "color": "#475569", "font_family": "Roboto", "alignment": "center"},

        # Samsung -4.5% (h=27 -> y=257..284, label y=237..252)
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "-4.5%", "x": 220, "y": 237, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#64748B", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 229, "y": 257, "width": 30, "height": 27, "background_color": "#94A3B8"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "삼성전자", "x": 214, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "color": "#64748B", "font_family": "Roboto", "alignment": "center"},

        # Right Panel
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "01  기술 · 시장 배경", "x": 312, "y": 96, "width": 363, "height": 18, "font_size": 11, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "실적 전 경계 매물로 아시아 반도체가 급락했으나, 엔비디아가 3Q 매출\n1,158억 달러·차세대 '베라 루빈' 폭발적 출발을 발표하며 불안을 불식", "x": 312, "y": 116, "width": 363, "height": 40, "font_size": 9.5, "color": "#334155", "font_family": "Roboto", "line_spacing": 140},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 312, "y": 162, "width": 363, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "02  수혜 및 타격 플레이어", "x": 312, "y": 170, "width": 363, "height": 18, "font_size": 11, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "수혜: TSMC 첨단 패키징(CoWoS)·광트랜시버·차세대 HBM 공급망\n부담: 범용 스마트폰·레거시 메모리 비중이 높은 부품사 마진 압박", "x": 312, "y": 190, "width": 363, "height": 40, "font_size": 9.5, "color": "#334155", "font_family": "Roboto", "line_spacing": 140},
        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "RECTANGLE", "x": 312, "y": 236, "width": 236, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-shape", "slide": "S_DEEP_CHIP", "shape_type": "ROUND_RECTANGLE", "x": 312, "y": 244, "width": 236, "height": 72, "background_color": "#EFF6FF"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "03  국내 IT · 비즈니스 시사점", "x": 320, "y": 249, "width": 220, "height": 16, "font_size": 10, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "베라 루빈 본격 가동으로 국내 HBM·첨단 기판\n수요는 탄탄하나 범용 메모리 현물가 약세는 변수.\n고부가 AI 메모리 믹스 전환 속도가 핵심 승부처", "x": 320, "y": 267, "width": 220, "height": 46, "font_size": 8.8, "bold": true, "color": "#0F172A", "font_family": "Roboto", "line_spacing": 135},

        {"op": "add-textbox", "slide": "S_DEEP_CHIP", "text": "팩트체크 근거: 엔비디아 FY27 3Q 실적발표·키플링어·빅고파이낸스 교차검증", "x": 45, "y": 320, "width": 500, "height": 15, "font_size": 8.2, "color": "#64748B", "font_family": "Roboto"},
        {"op": "set-notes", "slide": "S_DEEP_CHIP", "text": "두 번째는 인공지능 반도체 소식입니다. 실적 발표 직전만 해도 경계감에 에스케이하이닉스가 팔 퍼센트 가까이 급락했는데요. 막상 뚜껑을 열어보니 엔비디아 삼분기 매출이 천백오십팔억 달러, 전년 대비 백십일 퍼센트 급증했고, 차세대 칩 베라 루빈도 순항 중이라고 밝혔습니다. 국내 메모리 업계 역시 범용 제품 약세를 넘어 고부가 에이치비엠 중심으로 빠르게 체질을 전환하는 게 관건입니다."},

        # =====================================================================
        # SLIDE 5: 심층 분석 03 · 빅테크 · 클라우드 · SaaS
        # =====================================================================
        {"op": "add-slide", "layout": "BLANK", "id": "S_DEEP_CLOUD"},
        {"op": "set-background", "slide": "S_DEEP_CLOUD", "color": "#FFFFFF"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "심층 분석 03  ·  빅테크 · 클라우드 · SaaS  (5 / 8)", "x": 45, "y": 16, "width": 400, "height": 16, "font_size": 10, "bold": true, "color": "#0284C7", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "6일간 美 핵심 IT 7건 연쇄 장애… 7,200억 달러 투자 속 안정성 경고", "x": 45, "y": 33, "width": 630, "height": 28, "font_size": 20, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "MS 365·AWS 동부·워크데이·애플·항공·은행 동시다발 중단… 단일 클라우드 의존 리스크 현실화", "x": 45, "y": 63, "width": 630, "height": 18, "font_size": 11, "color": "#475569", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 45, "y": 86, "width": 630, "height": 1.5, "background_color": "#0F172A"},

        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "ROUND_RECTANGLE", "x": 45, "y": 94, "width": 250, "height": 222, "background_color": "#F8FAFC"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "도표 5. 빅테크 4사 데이터센터 CAPEX 추이", "x": 54, "y": 100, "width": 232, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},

        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "2024년 합산", "x": 52, "y": 120, "width": 64, "height": 15, "font_size": 7.8, "color": "#475569", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 118, "y": 122, "width": 36, "height": 10, "background_color": "#CBD5E1"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "2,400억$", "x": 160, "y": 120, "width": 56, "height": 15, "font_size": 7.8, "color": "#64748B", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "2026년 계획", "x": 52, "y": 140, "width": 64, "height": 15, "font_size": 7.8, "bold": true, "color": "#0F172A", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 118, "y": 142, "width": 94, "height": 10, "background_color": "#0284C7"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "7,200억$ (3배)", "x": 217, "y": 140, "width": 74, "height": 15, "font_size": 7.8, "bold": true, "color": "#0284C7", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "2027년 추정", "x": 52, "y": 160, "width": 64, "height": 15, "font_size": 7.8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 118, "y": 162, "width": 122, "height": 10, "background_color": "#1E3A8A"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "1.3조$", "x": 245, "y": 160, "width": 44, "height": 15, "font_size": 8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 54, "y": 182, "width": 232, "height": 1, "background_color": "#E2E8F0"},

        # Chart 6: Big Tech Single-Quarter AI Capex / Debt
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "도표 6. 빅테크 분기 투자·조달 규모 (억 달러)", "x": 54, "y": 188, "width": 232, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 54, "y": 207, "width": 232, "height": 100, "background_color": "#FFFFFF"},
        {"op": "add-line", "slide": "S_DEEP_CLOUD", "x": 64, "y": 284, "width": 212, "height": 0, "color": "#94A3B8", "line_weight": 1},

        # Amazon 530억 (h=48 -> y=236..284, label y=216..231)
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "530억$", "x": 66, "y": 216, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 75, "y": 236, "width": 30, "height": 48, "background_color": "#1E3A8A"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "아마존 3Q", "x": 60, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "bold": true, "color": "#0F172A", "font_family": "Roboto", "alignment": "center"},

        # Alphabet 514억 (h=46 -> y=238..284, label y=218..233)
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "514억$", "x": 144, "y": 218, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#0284C7", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 153, "y": 238, "width": 30, "height": 46, "background_color": "#0284C7"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "알파벳 3Q", "x": 138, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "bold": true, "color": "#475569", "font_family": "Roboto", "alignment": "center"},

        # MS Debt 250억 (h=24 -> y=260..284, label y=240..255)
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "250억$", "x": 220, "y": 240, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#64748B", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 229, "y": 260, "width": 30, "height": 24, "background_color": "#94A3B8"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "MS 채권조달", "x": 214, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "color": "#64748B", "font_family": "Roboto", "alignment": "center"},

        # Right Panel
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "01  기술 · 시장 배경", "x": 312, "y": 96, "width": 363, "height": 18, "font_size": 11, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "11월 12~17일 MS 365·AWS 미국 동부 인증 장애·애플 아이클라우드 등\n7건의 대형 장애가 연쇄 발생. AI 증설 경쟁 속 레거시 안정성 한계 노출", "x": 312, "y": 116, "width": 363, "height": 40, "font_size": 9.5, "color": "#334155", "font_family": "Roboto", "line_spacing": 140},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 312, "y": 162, "width": 363, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "02  수혜 및 타격 플레이어", "x": 312, "y": 170, "width": 363, "height": 18, "font_size": 11, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "수혜: 멀티 클라우드·관측성(Observability)·재해복구(DR) 솔루션 기업\n부담: 단일 리전·단일 인증(IAM)에 전사 업무를 의존하는 SaaS·금융사", "x": 312, "y": 190, "width": 363, "height": 40, "font_size": 9.5, "color": "#334155", "font_family": "Roboto", "line_spacing": 140},
        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "RECTANGLE", "x": 312, "y": 236, "width": 236, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-shape", "slide": "S_DEEP_CLOUD", "shape_type": "ROUND_RECTANGLE", "x": 312, "y": 244, "width": 236, "height": 72, "background_color": "#EFF6FF"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "03  국내 IT · 비즈니스 시사점", "x": 320, "y": 249, "width": 220, "height": 16, "font_size": 10, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "앱이 정상이어도 인증 시스템이 멈추면 업무 마비.\n사내 핵심 서비스의 이중화(Multi-Region)와\n장애 대응 매뉴얼 재점검이 즉각 필요한 시점", "x": 320, "y": 267, "width": 220, "height": 46, "font_size": 8.8, "bold": true, "color": "#0F172A", "font_family": "Roboto", "line_spacing": 135},

        {"op": "add-textbox", "slide": "S_DEEP_CLOUD", "text": "팩트체크 근거: 테크리퍼블릭 장애 타임라인·뉴욕타임스·S&P글로벌 교차검증", "x": 45, "y": 320, "width": 500, "height": 15, "font_size": 8.2, "color": "#64748B", "font_family": "Roboto"},
        {"op": "set-notes", "slide": "S_DEEP_CLOUD", "text": "세 번째는 클라우드와 빅테크 이슈입니다. 지난 육일 동안 마이크로소프트 삼육오와 아마존 웹 서비스 미국 동부, 애플 아이클라우드, 미국 은행과 항공망까지 일곱 건의 대형 장애가 줄줄이 터졌습니다. 빅테크 사사가 올해만 칠천이백억 달러를 데이터센터에 쏟아붓고 있지만, 정작 단일 인증 시스템이 멈추면 전사 업무가 마비되는 구조적 취약점이 드러난 만큼 우리 인프라의 이중화 점검이 필요합니다."},

        # =====================================================================
        # SLIDE 6: 심층 분석 04 · 피지컬 AI · 보안 · 테크 정책
        # =====================================================================
        {"op": "add-slide", "layout": "BLANK", "id": "S_DEEP_POLICY"},
        {"op": "set-background", "slide": "S_DEEP_POLICY", "color": "#FFFFFF"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "심층 분석 04  ·  피지컬 AI · 보안 · 정책  (6 / 8)", "x": 45, "y": 16, "width": 400, "height": 16, "font_size": 10, "bold": true, "color": "#0284C7", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "오픈AI 안전심사 의무화 · 캘리포니아 SB 813 · 유로폴 사이버 소탕", "x": 45, "y": 33, "width": 630, "height": 28, "font_size": 20, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "프런티어 AI 출시 전 4단계 검증 체계 도입 및 글로벌 AI 안전·사이버범죄 공동 대응 격상", "x": 45, "y": 63, "width": 630, "height": 18, "font_size": 11, "color": "#475569", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 45, "y": 86, "width": 630, "height": 1.5, "background_color": "#0F172A"},

        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "ROUND_RECTANGLE", "x": 45, "y": 94, "width": 250, "height": 222, "background_color": "#F8FAFC"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "도표 7. 오픈AI 4계층 모델 안전 검증 구조", "x": 54, "y": 100, "width": 232, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},

        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "1단계 연구·격리", "x": 52, "y": 120, "width": 70, "height": 15, "font_size": 7.6, "bold": true, "color": "#0F172A", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 124, "y": 122, "width": 108, "height": 10, "background_color": "#1E3A8A"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "샌드박스", "x": 238, "y": 120, "width": 50, "height": 15, "font_size": 7.6, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "2단계 내부배포", "x": 52, "y": 140, "width": 70, "height": 15, "font_size": 7.6, "bold": true, "color": "#0F172A", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 124, "y": 142, "width": 96, "height": 10, "background_color": "#0284C7"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "정렬·차단", "x": 226, "y": 140, "width": 54, "height": 15, "font_size": 7.6, "bold": true, "color": "#0284C7", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "3단계 외부출시", "x": 52, "y": 160, "width": 70, "height": 15, "font_size": 7.6, "color": "#475569", "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 124, "y": 162, "width": 84, "height": 10, "background_color": "#64748B"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "상시감시", "x": 214, "y": 160, "width": 54, "height": 15, "font_size": 7.6, "color": "#475569", "font_family": "Roboto", "content_alignment": "MIDDLE"},

        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 54, "y": 182, "width": 232, "height": 1, "background_color": "#E2E8F0"},

        # Chart 8: Europol Operation TorNado Results
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "도표 8. 유로폴 14개국 사이버 합동작전 성과", "x": 54, "y": 188, "width": 232, "height": 16, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 54, "y": 207, "width": 232, "height": 100, "background_color": "#FFFFFF"},
        {"op": "add-line", "slide": "S_DEEP_POLICY", "x": 64, "y": 284, "width": 212, "height": 0, "color": "#94A3B8", "line_weight": 1},

        # 354 arrests (h=48 -> y=236..284, label y=216..231)
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "354명", "x": 66, "y": 216, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 75, "y": 236, "width": 30, "height": 48, "background_color": "#1E3A8A"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "용의자 체포", "x": 60, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "bold": true, "color": "#0F172A", "font_family": "Roboto", "alignment": "center"},

        # 257 domains (h=35 -> y=249..284, label y=229..244)
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "257개", "x": 144, "y": 229, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#0284C7", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 153, "y": 249, "width": 30, "height": 35, "background_color": "#0284C7"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "악성 도메인", "x": 138, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "color": "#475569", "font_family": "Roboto", "alignment": "center"},

        # 235 servers (h=32 -> y=252..284, label y=232..247)
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "235대", "x": 220, "y": 232, "width": 48, "height": 15, "font_size": 8, "bold": true, "color": "#64748B", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 229, "y": 252, "width": 30, "height": 32, "background_color": "#64748B"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "범죄 서버", "x": 214, "y": 287, "width": 60, "height": 15, "font_size": 7.2, "color": "#64748B", "font_family": "Roboto", "alignment": "center"},

        # Right Panel
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "01  기술 · 시장 배경", "x": 312, "y": 96, "width": 363, "height": 18, "font_size": 11, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "오픈AI가 11/18 미충족 시 학습 중단·출시 보류하는 안전 심사를 공식화,\n캘리포니아도 독립 검증기관 인증법(SB 813) 후속 지침을 발표", "x": 312, "y": 116, "width": 363, "height": 40, "font_size": 9.5, "color": "#334155", "font_family": "Roboto", "line_spacing": 140},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 312, "y": 162, "width": 363, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "02  수혜 및 타격 플레이어", "x": 312, "y": 170, "width": 363, "height": 18, "font_size": 11, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "수혜: AI 레드팀·거버넌스 평가·보안 자동화(SecOps) 전문 기업\n부담: 안전 검증 비용·출시 지연이 커진 프런티어 모델 개발사", "x": 312, "y": 190, "width": 363, "height": 40, "font_size": 9.5, "color": "#334155", "font_family": "Roboto", "line_spacing": 140},
        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "RECTANGLE", "x": 312, "y": 236, "width": 236, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-shape", "slide": "S_DEEP_POLICY", "shape_type": "ROUND_RECTANGLE", "x": 312, "y": 244, "width": 236, "height": 72, "background_color": "#EFF6FF"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "03  국내 IT · 비즈니스 시사점", "x": 320, "y": 249, "width": 220, "height": 16, "font_size": 10, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "EU AI법 집행과 미국 주별 규제(전 세계 1,170건)\n가 겹치며 글로벌 진출 시 AI 안전 감사·로그 보관\n체계 구축이 선택이 아닌 필수 요건으로 정착", "x": 320, "y": 267, "width": 220, "height": 46, "font_size": 8.8, "bold": true, "color": "#0F172A", "font_family": "Roboto", "line_spacing": 135},

        {"op": "add-textbox", "slide": "S_DEEP_POLICY", "text": "팩트체크 근거: 오픈AI 공식 발표·캘리포니아 주정부·유로폴 보도자료 교차검증", "x": 45, "y": 320, "width": 500, "height": 15, "font_size": 8.2, "color": "#64748B", "font_family": "Roboto"},
        {"op": "set-notes", "slide": "S_DEEP_POLICY", "text": "네 번째는 인공지능 안전과 사이버보안입니다. 오픈에이아이가 안전 기준에 못 미치면 학습을 멈추고 출시를 보류하는 사단계 심사 체계를 발표했고, 캘리포니아주도 독립 검증기관을 인증하는 후속 지침을 내놨습니다. 한편 유로폴은 십사개국 공조로 악성 서버 이백삼십오 대를 압수하며 보안 대응을 끌어올렸습니다. 이제 글로벌 서비스를 준비할 때 인공지능 안전 검증과 로깅은 필수 관문입니다."},

        # =====================================================================
        # SLIDE 7: 주간 IT·AI 주요 단신 브리핑 8선 (Quick Radar)
        # Left Col (x=45..345): Items 01~04 (y=78..330)
        # Right Col: Items 05~07 (x=365..675, y=78..248 -> above PiP y=256)
        #            Item 08 (x=365..548, y=256..330 -> left of PiP x=560)
        # =====================================================================
        {"op": "add-slide", "layout": "BLANK", "id": "S_RADAR"},
        {"op": "set-background", "slide": "S_RADAR", "color": "#FFFFFF"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "주간 IT · AI 주요 단신 브리핑 8선  (7 / 8)", "x": 45, "y": 18, "width": 400, "height": 16, "font_size": 10, "bold": true, "color": "#0284C7", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "놓치면 안 될 분야별 주간 핵심 테크 레이더", "x": 45, "y": 35, "width": 630, "height": 28, "font_size": 20, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_RADAR", "shape_type": "RECTANGLE", "x": 45, "y": 70, "width": 630, "height": 1.5, "background_color": "#0F172A"},
        {"op": "add-line", "slide": "S_RADAR", "x": 355, "y": 78, "width": 0, "height": 252, "color": "#E2E8F0", "line_weight": 1},

        # Left Column: 01~04
        {"op": "add-textbox", "slide": "S_RADAR", "text": "01  [오픈소스·모델] 구글 딥마인드, 월드모델 '지니 4' 정식 공개", "x": 45, "y": 78, "width": 302, "height": 17, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "상호작용 가상세계를 실시간 생성하는 차세대 월드모델 정식 출시,\n로보틱스 시뮬레이션·게임 제작 패러다임 가속  (딥마인드 블로그)", "x": 45, "y": 95, "width": 302, "height": 34, "font_size": 8.4, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "add-shape", "slide": "S_RADAR", "shape_type": "RECTANGLE", "x": 45, "y": 134, "width": 298, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_RADAR", "text": "02  [스타트업·VC] 오픈AI, 상장 2027년 연기·1.25조$ 투자 추진", "x": 45, "y": 141, "width": 302, "height": 17, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "앤스로픽 상장 맞서 기업가치 1.25조 달러 민간 라운드 조달 중,\n연말 연환산 매출 700억 달러 이상 달성 목표 제시  (외신 종합)", "x": 45, "y": 158, "width": 302, "height": 34, "font_size": 8.4, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "add-shape", "slide": "S_RADAR", "shape_type": "RECTANGLE", "x": 45, "y": 197, "width": 298, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_RADAR", "text": "03  [국내 AI·반도체] 메모리 현물가 약세 속 HBM4 수주전 가속", "x": 45, "y": 204, "width": 302, "height": 17, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "범용 D램 현물가 하락으로 단기 변동성이 커졌으나, 엔비디아 차세대\n루빈 플랫폼용 HBM4 조기 양산 경쟁 본격화  (빅고파이낸스)", "x": 45, "y": 221, "width": 302, "height": 34, "font_size": 8.4, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "add-shape", "slide": "S_RADAR", "shape_type": "RECTANGLE", "x": 45, "y": 260, "width": 298, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_RADAR", "text": "04  [디바이스·엣지] 엔비디아 엣지AI 매출 82억$·DGX 스파크 공개", "x": 45, "y": 267, "width": 302, "height": 17, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "엣지 컴퓨팅 분기 매출이 전년 대비 42% 급증, 책상 위 초소형 AI\n슈퍼컴퓨터 개발키트 'DGX 스파크'로 로컬 AI 확산  (엔비디아)", "x": 45, "y": 284, "width": 302, "height": 34, "font_size": 8.4, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},

        # Right Column: 05~07 (full width x=365..675, y=78..248 -> ends strictly above Avatar PiP y=256!)
        {"op": "add-textbox", "slide": "S_RADAR", "text": "05  [클라우드·데이터] MS, 바이트댄스와 5억$ 애저 AI 계약 임박", "x": 365, "y": 78, "width": 310, "height": 17, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "중국 빅테크의 해외 AI 연산 수요 확보 움직임 속 미·중 기술 통제\n논란과 클라우드 대형 수주 간 줄다리기 심화  (24/7 월스트리트)", "x": 365, "y": 95, "width": 310, "height": 34, "font_size": 8.4, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "add-shape", "slide": "S_RADAR", "shape_type": "RECTANGLE", "x": 365, "y": 133, "width": 305, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_RADAR", "text": "06  [사이버보안] 데이터센터 물리적 침입 위협, 사이버범죄 추월", "x": 365, "y": 139, "width": 310, "height": 17, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "초대형 AI 데이터센터가 국가 핵심 자산으로 격상되며 물리 보안·\n호주-미국 AI 공급망 보안 협정 참여 등 대응 확대  (호주사이버매거진)", "x": 365, "y": 156, "width": 310, "height": 34, "font_size": 8.4, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "add-shape", "slide": "S_RADAR", "shape_type": "RECTANGLE", "x": 365, "y": 194, "width": 305, "height": 1, "background_color": "#E2E8F0"},

        {"op": "add-textbox", "slide": "S_RADAR", "text": "07  [로보틱스·과학AI] 엔비디아 '루빈 HPC'·과학 에이전트 공개", "x": 365, "y": 200, "width": 310, "height": 17, "font_size": 9, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "양자컴퓨팅 연동 Slurm 확장 및 CUDA-X 과학 에이전트 발표,\n신약·신소재·피지컬 AI 연구 속도 혁신 예고  (엔비디아 블로그)", "x": 365, "y": 217, "width": 310, "height": 31, "font_size": 8.4, "color": "#334155", "font_family": "Roboto", "line_spacing": 130},
        {"op": "add-shape", "slide": "S_RADAR", "shape_type": "RECTANGLE", "x": 365, "y": 252, "width": 183, "height": 1, "background_color": "#E2E8F0"},

        # Item 08 Compact Box (x=365..548, y=257..330 -> strictly left of Avatar PiP x=560!)
        {"op": "add-textbox", "slide": "S_RADAR", "text": "08  [AI 정책·영국] 英 의회 안전 촉구", "x": 365, "y": 257, "width": 183, "height": 17, "font_size": 8.8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_RADAR", "text": "영국 의회 위원회, 4천억 파운드\nAI 성장 기회 확보 위해 빅테크의\n안전 공백 조속 해소 촉구  (영국의회)", "x": 365, "y": 274, "width": 183, "height": 48, "font_size": 8.1, "color": "#334155", "font_family": "Roboto", "line_spacing": 135},
        {"op": "set-notes", "slide": "S_RADAR", "text": "놓치면 안 될 주간 테크 단신도 빠르게 훑어보겠습니다. 구글 딥마인드가 실시간 가상세계 모델 지니 포를 정식 공개했고, 오픈에이아이는 상장을 이천이십칠년으로 미루고 대규모 민간 자금을 유치 중입니다. 엔비디아는 책상 위 인공지능 슈퍼컴퓨터 디지엑스 스파크와 과학 에이전트용 루빈 에이치피시를 발표했으며, 마이크로소프트의 오억 달러 규모 애저 계약과 데이터센터 물리 보안 위협 부각도 주목할 대목입니다."},

        # =====================================================================
        # SLIDE 8: 주간 종합 분석 · 도표 9 매트릭스 + 향후 테크 일정 + 팀 액션
        # Top Banner: y=76..112
        # Left Panel (x=45..265, y=120..330): 도표 9 (2x2 Matrix)
        # Right-Top Table (x=280..675, y=120..246): 향후 핵심 테크 일정 (above PiP y=256!)
        # Bottom-Center Action Box (x=280..548, y=256..330): 팀 액션 체크포인트 (left of PiP x=560!)
        # Right-Bottom (x=560..720, y=256..405): Closing Avatar PiP Safe Zone!
        # =====================================================================
        {"op": "add-slide", "layout": "BLANK", "id": "S_WATCH"},
        {"op": "set-background", "slide": "S_WATCH", "color": "#FFFFFF"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "주간 종합 분석 및 향후 테크 일정  (8 / 8)", "x": 45, "y": 18, "width": 400, "height": 16, "font_size": 10, "bold": true, "color": "#0284C7", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "주간 핵심 흐름 · 파급력 매트릭스 및 다음 주 분수령", "x": 45, "y": 35, "width": 630, "height": 28, "font_size": 20, "bold": true, "color": "#0F172A", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_WATCH", "shape_type": "RECTANGLE", "x": 45, "y": 70, "width": 630, "height": 1.5, "background_color": "#0F172A"},

        {"op": "add-textbox", "slide": "S_WATCH", "text": "주간 핵심 흐름  |  AI 수익화 증명(앤스로픽 상장) → 인프라 검증(엔비디아 1,158억$) → 안정성·규제(클라우드 장애·SB 813)", "x": 45, "y": 78, "width": 630, "height": 30, "font_size": 9.8, "bold": true, "color": "#0F172A", "background_color": "#F8FAFC", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},

        # Left Panel: 도표 9 (2x2 Matrix, x=45..265, y=116..330)
        {"op": "add-shape", "slide": "S_WATCH", "shape_type": "ROUND_RECTANGLE", "x": 45, "y": 116, "width": 220, "height": 214, "background_color": "#F8FAFC"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "도표 9. 우리 조직 파급력 × 시급성 분석", "x": 53, "y": 122, "width": 204, "height": 15, "font_size": 8.8, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-shape", "slide": "S_WATCH", "shape_type": "RECTANGLE", "x": 63, "y": 141, "width": 186, "height": 165, "background_color": "#FFFFFF"},

        {"op": "add-line", "slide": "S_WATCH", "x": 156, "y": 141, "width": 0, "height": 165, "color": "#CBD5E1", "line_weight": 1, "dash_style": "DASH"},
        {"op": "add-line", "slide": "S_WATCH", "x": 63, "y": 223, "width": 186, "height": 0, "color": "#CBD5E1", "line_weight": 1, "dash_style": "DASH"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "↑ 파급력 (높음)", "x": 66, "y": 143, "width": 85, "height": 13, "font_size": 7.2, "color": "#64748B", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "시급성 (높음) →", "x": 163, "y": 291, "width": 82, "height": 13, "font_size": 7.2, "color": "#64748B", "font_family": "Roboto", "alignment": "right"},

        {"op": "add-textbox", "slide": "S_WATCH", "text": "03 클라우드 장애\n(이중화 점검)", "x": 162, "y": 153, "width": 82, "height": 27, "font_size": 7.2, "bold": true, "color": "#FFFFFF", "background_color": "#DC2626", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE", "line_spacing": 112},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "01 앤스로픽 IPO", "x": 162, "y": 189, "width": 82, "height": 22, "font_size": 7.2, "bold": true, "color": "#FFFFFF", "background_color": "#1E3A8A", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "02 엔비디아 루빈", "x": 70, "y": 173, "width": 80, "height": 22, "font_size": 7.2, "bold": true, "color": "#FFFFFF", "background_color": "#0284C7", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "04 AI 안전·규제", "x": 162, "y": 236, "width": 82, "height": 22, "font_size": 7.2, "bold": true, "color": "#0F172A", "background_color": "#E2E8F0", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "우상단(적색/인디고): 즉각 점검 대상", "x": 55, "y": 311, "width": 200, "height": 15, "font_size": 7.4, "color": "#475569", "font_family": "Roboto", "alignment": "center"},

        # Right-Top Schedule Table (x=280..675, y=116..234 -> 18pt clean gap above checkpoint card & Avatar PiP!)
        {"op": "add-table", "slide": "S_WATCH", "rows": 4, "cols": 3, "id": "T_WATCH", "x": 280, "y": 116, "width": 395, "height": 112},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 0, "col": 0, "text": "예정 일정", "bold": true, "font_size": 8.6, "color": "#0F172A", "background_color": "#F1F5F9", "font_family": "Roboto"},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 0, "col": 1, "text": "핵심 IT · AI 분수령", "bold": true, "font_size": 8.6, "color": "#0F172A", "background_color": "#F1F5F9", "font_family": "Roboto"},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 0, "col": 2, "text": "주요 점검 포인트", "bold": true, "font_size": 8.6, "color": "#0F172A", "background_color": "#F1F5F9", "font_family": "Roboto"},

        {"op": "set-table-cell", "table": "T_WATCH", "row": 1, "col": 0, "text": "11월 19일", "bold": true, "font_size": 8.2, "color": "#DC2626", "background_color": "#FFFFFF", "font_family": "Roboto"},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 1, "col": 1, "text": "앤스로픽 나스닥 첫 거래", "bold": true, "font_size": 8.2, "color": "#0F172A", "background_color": "#FFFFFF", "font_family": "Roboto"},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 1, "col": 2, "text": "공모가 상회 여부 · AI SW 파급", "font_size": 8.0, "color": "#334155", "background_color": "#FFFFFF", "font_family": "Roboto"},

        {"op": "set-table-cell", "table": "T_WATCH", "row": 2, "col": 0, "text": "11월 하순", "bold": true, "font_size": 8.2, "color": "#1E3A8A", "background_color": "#FFFFFF", "font_family": "Roboto"},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 2, "col": 1, "text": "美 클라우드 장애 보고서", "bold": true, "font_size": 8.2, "color": "#0F172A", "background_color": "#FFFFFF", "font_family": "Roboto"},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 2, "col": 2, "text": "AWS·MS 인증 장애 원인 · SLA", "font_size": 8.0, "color": "#334155", "background_color": "#FFFFFF", "font_family": "Roboto"},

        {"op": "set-table-cell", "table": "T_WATCH", "row": 3, "col": 0, "text": "12월 초", "bold": true, "font_size": 8.2, "color": "#0284C7", "background_color": "#FFFFFF", "font_family": "Roboto"},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 3, "col": 1, "text": "AWS 리인벤트 2026", "bold": true, "font_size": 8.2, "color": "#0F172A", "background_color": "#FFFFFF", "font_family": "Roboto"},
        {"op": "set-table-cell", "table": "T_WATCH", "row": 3, "col": 2, "text": "자체 AI 칩 · 에이전트 신제품", "font_size": 8.0, "color": "#334155", "background_color": "#FFFFFF", "font_family": "Roboto"},

        # Bottom-Center Team Action Box (x=280..548, y=262..330 -> crisp gap below table, left of PiP x=560!)
        {"op": "add-shape", "slide": "S_WATCH", "shape_type": "ROUND_RECTANGLE", "x": 280, "y": 262, "width": 268, "height": 68, "background_color": "#EFF6FF"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "이번 주 팀 체크포인트", "x": 290, "y": 266, "width": 248, "height": 15, "font_size": 9.2, "bold": true, "color": "#1E3A8A", "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S_WATCH", "text": "① 핵심 사내 클라우드·인증(SSO) 이중화 상태 점검\n② 에이전트 도입 시 정량 ROI 지표(절감시간) 설정\n③ 글로벌 출시 AI 기능의 안전 로그·감사 체계 확인", "x": 290, "y": 283, "width": 250, "height": 44, "font_size": 8.2, "bold": true, "color": "#0F172A", "font_family": "Roboto", "line_spacing": 135},
        {"op": "set-notes", "slide": "S_WATCH", "text": "마지막으로 이번 주 흐름을 한 줄로 정리하면, 인공지능 산업은 확실한 수익화 증명과 초대형 인프라 투자, 그리고 안정성과 안전 규제가 동시에 맞물리는 성숙기에 진입했습니다. 다음 주에는 앤스로픽 상장 첫 거래 흐름과 미국 클라우드 장애 보고서를 주목해 주시고요. 이상으로 주간 아이티 에이아이 브리핑을 마칩니다. 다음 주 수요일 오전 열 시에 다시 찾아뵙겠습니다. 감사합니다."},
    ])

    batch_path = "/tmp/ai_weekly_8slide_batch.json"
    with open(batch_path, "w", encoding="utf-8") as f:
        json.dump(ops, f, ensure_ascii=False, indent=2)

    subprocess.run(["gslides", "mutate", "batch", PRES_ID, "-f", batch_path, "--json"], check=True)
    subprocess.run(["gslides", "readonly", "export", PRES_ID, PDF_OUT_PATH, "--format", "pdf"], check=True)
    print(f"[OK] Built 8-slide video-optimized deck ({PRES_ID}) and exported PDF -> {PDF_OUT_PATH}")


if __name__ == "__main__":
    build_deck()
