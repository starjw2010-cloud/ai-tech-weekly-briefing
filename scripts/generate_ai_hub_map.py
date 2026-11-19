#!/usr/bin/env python3
"""
글로벌 IT · AI 거점 세계지도 정밀 좌표 타깃팅(◎) 및 인출선(Leader Line) 생성 스크립트
- 원본 베이스 지도: world_map_base.png (1200x896)
- IT·AI 핵심 거점 좌표 (실리콘밸리, 미국 동부, 유럽, 영국, 중국, 대만 TSMC, 한국 HBM, 일본) 지원
"""
from PIL import Image, ImageDraw, ImageFont
import math

# 1200x896 원본 지도 기준 글로벌 IT·AI 주요 거점 픽셀 좌표 사전
TECH_HUB_COORDS_1200x896 = {
    "SILICON_VALLEY": (172, 396),  # 미국 캘리포니아 (실리콘밸리 · OpenAI · Anthropic · NVIDIA · Google)
    "US_EAST":        (272, 385),  # 미국 동부 (워싱턴 DC 규제 · 뉴욕 월가 · AWS US-East-1)
    "US":             (225, 392),  # 미국 본토 중앙
    "UK":             (565, 332),  # 영국 (런던 · DeepMind · 영국 의회 AI 안전)
    "EU":             (595, 352),  # 유럽연합 (브뤼셀 EU AI Act · 유로폴)
    "CHINA":          (915, 398),  # 중국 (베이징·항저우·선전 오픈웨이트 AI)
    "TAIWAN":         (978, 445),  # 대만 (TSMC 파운드리 · CoWoS 패키징)
    "KOREA":          (989, 395),  # 대한민국 (서울·판교·평택·이천 HBM·국내 AI)
    "JAPAN":          (1035, 398), # 일본 (도쿄 AI 인프라)
    "SINGAPORE":      (925, 530),  # 싱가포르 (동남아 AI 데이터센터 허브)
    "INDIA":          (825, 455),  # 인도 (벵갈루루 AI 개발·클라우드)
    "MIDDLE_EAST":    (705, 425),  # 중동 (UAE·사우디 소버린 AI 펀드)
}

Y_OFFSET = 75
INDIGO = (30, 58, 138, 255)     # #1E3A8A (딥 인디고)
CYAN = (2, 132, 199, 255)       # #0284C7 (테크 시안)
RED = (220, 38, 38, 255)        # #DC2626 (한국 강조)
WHITE = (255, 255, 255, 255)


def get_cropped_coord(key_or_tuple):
    if isinstance(key_or_tuple, str):
        px, py = TECH_HUB_COORDS_1200x896[key_or_tuple]
    else:
        px, py = key_or_tuple
    return (px, py - Y_OFFSET)


def draw_curved_dashed_arc(draw, p1, p2, bend=-60, color=CYAN, width=3, dash_len=12, gap_len=8):
    mx = (p1[0] + p2[0]) / 2.0
    my = (p1[1] + p2[1]) / 2.0 + bend
    steps = 120
    curve_pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p1[0] + 2 * (1 - t) * t * mx + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p1[1] + 2 * (1 - t) * t * my + t ** 2 * p2[1]
        curve_pts.append((x, y))
    dist_acc = 0.0
    drawing = True
    for i in range(len(curve_pts) - 1):
        x0, y0 = curve_pts[i]
        x1, y1 = curve_pts[i + 1]
        seg = math.hypot(x1 - x0, y1 - y0)
        if drawing:
            draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
        dist_acc += seg
        if drawing and dist_acc >= dash_len:
            drawing = False
            dist_acc = 0.0
        elif not drawing and dist_acc >= gap_len:
            drawing = True
            dist_acc = 0.0


def add_pin_and_callout(draw, font_bold, pt, badge_center, text, color=INDIGO, is_korea=False):
    px, py = pt
    bx, by = badge_center
    draw.line([(px, py), (bx, by)], fill=color, width=3)

    r_outer = 14 if is_korea else 12
    r_inner = 6 if is_korea else 5
    draw.ellipse(
        [px - r_outer, py - r_outer, px + r_outer, py + r_outer],
        fill=(color[0], color[1], color[2], 75),
        outline=color,
        width=2,
    )
    draw.ellipse(
        [px - r_inner, py - r_inner, px + r_inner, py + r_inner],
        fill=color,
        outline=WHITE,
        width=2,
    )

    bbox = draw.textbbox((0, 0), text, font=font_bold)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 16, 10
    rx0 = bx - tw // 2 - pad_x
    ry0 = by - th // 2 - pad_y
    rx1 = bx + tw // 2 + pad_x
    ry1 = by + th // 2 + pad_y

    draw.rounded_rectangle([rx0 - 2, ry0 - 2, rx1 + 2, ry1 + 2], radius=8, fill=WHITE)
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=7, fill=color)
    draw.text((bx - tw // 2, by - th // 2 - 3), text, font=font_bold, fill=WHITE)


def render_ai_hub_map(base_map_path, output_path, pins, arcs):
    """
    pins: [{"coord": "SILICON_VALLEY", "badge": (bx, by), "text": "01 실리콘밸리", "color": INDIGO, "is_korea": False}, ...]
    arcs: [{"from": "SILICON_VALLEY", "to": "TAIWAN", "bend": -85, "color": CYAN}, ...]
    """
    base = Image.open(base_map_path).convert("RGBA")
    im = base.crop((0, Y_OFFSET, 1200, 825))
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_bold = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 22)

    for arc in arcs:
        p1 = get_cropped_coord(arc["from"])
        p2 = get_cropped_coord(arc["to"])
        if arc.get("solid"):
            draw.line([p1, p2], fill=arc.get("color", RED), width=4)
        else:
            draw_curved_dashed_arc(
                draw, p1, p2, bend=arc.get("bend", -65), color=arc.get("color", CYAN), width=3
            )

    for pin in pins:
        pt = get_cropped_coord(pin["coord"])
        is_k = pin.get("is_korea", False)
        col = RED if is_k else pin.get("color", INDIGO)
        add_pin_and_callout(draw, font_bold, pt, pin["badge"], pin["text"], color=col, is_korea=is_k)

    out = Image.alpha_composite(im, overlay).convert("RGB")
    out.save(output_path, quality=95)
    return output_path


if __name__ == "__main__":
    # 이번 주(2026.11.12~11.19) 글로벌 IT·AI 4대 거점 + 한국 파급 지도 생성
    default_pins = [
        {"coord": "SILICON_VALLEY", "badge": (195, 195), "text": "01 실리콘밸리 (IPO·AI안전)", "color": INDIGO},
        {"coord": "US_EAST",        "badge": (290, 485), "text": "03 미 동부 (클라우드 장애)", "color": CYAN},
        {"coord": "EU",             "badge": (605, 165), "text": "04 유럽·영국 (AI 규제·보안)", "color": INDIGO},
        {"coord": "TAIWAN",         "badge": (955, 520), "text": "02 대만 TSMC (CoWoS)", "color": CYAN},
        {"coord": "KOREA",          "badge": (1010, 210), "text": "한국 (HBM·AI 파급)", "is_korea": True},
    ]
    default_arcs = [
        {"from": "SILICON_VALLEY", "to": "TAIWAN", "bend": 110, "color": CYAN},
        {"from": "TAIWAN", "to": "KOREA", "bend": -30, "color": RED, "solid": True},
        {"from": "SILICON_VALLEY", "to": "EU", "bend": -85, "color": INDIGO},
        {"from": "US_EAST", "to": "KOREA", "bend": -110, "color": CYAN},
    ]
    render_ai_hub_map("/tmp/world_map_base.png", "/tmp/ai_hub_map_annotated.png", default_pins, default_arcs)
    print("[OK] Generated /tmp/ai_hub_map_annotated.png")
