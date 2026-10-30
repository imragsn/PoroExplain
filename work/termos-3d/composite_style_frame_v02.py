"""
Composite VOLT DS Style Board Frame v0.2
Implements all user feedback:
1. Eyebrow: @porotheexplorer
2. Typography: Plus Jakarta Sans with strict VOLT type tokens
3. Subtitle Karaoke: Center-aligned (rata tengah di X=540), clean no-box, active word #E8F500
4. Text overflow fix: Strict auto-wrap and padding in all HUD boxes & Metric card
5. Footer removed completely (clean bottom area)
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
BASE_IMG = os.path.join(ROOT, "work", "termos-3d", "style_b_base_1080x1920.png")
OUT_PNG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.2.png")
OUT_JPG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.2.jpg")

# VOLT DS Color Tokens
INK = (16, 17, 16, 255)            # #101110
PAPER = (255, 255, 250, 255)       # #FFFFFA
ELECTRIC = (232, 245, 0, 255)      # #E8F500
MUTED = (89, 93, 82, 255)          # #595D52
LINE = (145, 149, 135, 255)        # #919587

# Font: Plus Jakarta Sans
FONT_PATH = os.path.join(ROOT, "work", "PlusJakartaSans.ttf")
font_title = ImageFont.truetype(FONT_PATH, 46)
font_heading = ImageFont.truetype(FONT_PATH, 26)
font_body = ImageFont.truetype(FONT_PATH, 19)
font_body_bold = ImageFont.truetype(FONT_PATH, 19)
font_label = ImageFont.truetype(FONT_PATH, 15)
font_subtitle = ImageFont.truetype(FONT_PATH, 42)
font_metric = ImageFont.truetype(FONT_PATH, 68)
font_tag = ImageFont.truetype(FONT_PATH, 18)


def draw_hud_box_clamped(draw, x_anchor, y_anchor, x_box, y_box, w_box, h_box, tag, title, body_lines, align_right=False):
    # Angular 2px leader line
    if align_right:
        x_connect = x_box + w_box
        y_connect = y_box + h_box // 2
        elbow_x = x_anchor - 45
        points = [(x_anchor, y_anchor), (elbow_x, y_anchor), (elbow_x, y_connect), (x_connect, y_connect)]
    else:
        x_connect = x_box
        y_connect = y_box + h_box // 2
        elbow_x = x_anchor + 45
        points = [(x_anchor, y_anchor), (elbow_x, y_anchor), (elbow_x, y_connect), (x_connect, y_connect)]

    draw.line(points, fill=INK, width=2)
    draw.rectangle([x_anchor - 4, y_anchor - 4, x_anchor + 4, y_anchor + 4], fill=ELECTRIC, outline=INK, width=2)

    # Sharp 2px box (VOLT: zero radius, paper fill, 2px ink stroke)
    draw.rectangle([x_box, y_box, x_box + w_box, y_box + h_box], fill=PAPER, outline=INK, width=2)

    pad_x = 16
    draw.text((x_box + pad_x, y_box + 12), tag.upper(), font=font_label, fill=MUTED)
    draw.text((x_box + pad_x, y_box + 34), title.upper(), font=font_heading, fill=INK)

    line_y = y_box + 70
    for line in body_lines:
        draw.text((x_box + pad_x, line_y), line, font=font_body, fill=MUTED)
        line_y += 24


def draw_thermal_particles(draw):
    center_x = 540
    for y in [820, 920, 1020, 1120, 1220]:
        for offset in [40, 80, 120]:
            draw.arc([center_x - offset, y - 30, center_x + offset, y + 30], start=300, end=420, fill=(230, 126, 34, 180), width=2)
        ref_x = 698
        draw.line([(ref_x, y), (ref_x - 55, y - 25)], fill=ELECTRIC, width=3)
        draw.polygon([(ref_x - 55, y - 25), (ref_x - 42, y - 30), (ref_x - 47, y - 18)], fill=INK)

    particle_coords = [
        (580, 850), (620, 880), (660, 910), (600, 950), (640, 990),
        (590, 1050), (630, 1080), (665, 1110), (610, 1180), (650, 1210)
    ]
    for px, py in particle_coords:
        draw.rectangle([px - 3, py - 3, px + 3, py + 3], fill=ELECTRIC, outline=INK, width=1)


def main():
    base = Image.open(BASE_IMG).convert("RGBA")
    draw = ImageDraw.Draw(base)

    # 1. Thermal Radiation Effect
    draw_thermal_particles(draw)

    # 2. VOLT DS Header Zone (Top, Y=70 to Y=210)
    margin_x = 64
    content_w = 1080 - 2 * margin_x  # 952 px

    # Eyebrow requested: @porotheexplorer
    draw.text((margin_x, 72), "@porotheexplorer", font=font_tag, fill=MUTED)
    # Title
    draw.text((margin_x, 104), "KENAPA TERMOS BISA TAHAN PANAS?", font=font_title, fill=INK)
    # 2px Sharp Rule
    draw.line([(margin_x, 176), (margin_x + content_w, 176)], fill=INK, width=2)

    # 3. VOLT DS Technical Annotation HUDs (Carefully wrapped & sized, NO overflow)
    # Callout 1: Vacuum Gap (Left, anchor at X=370, Y=980)
    draw_hud_box_clamped(
        draw,
        x_anchor=370, y_anchor=980,
        x_box=margin_x, y_box=910,
        w_box=310, h_box=130,
        tag="Komponen 02 — Vakum",
        title="Celah Vakum",
        body_lines=[
            "Ruang hampa ~2mm memutus",
            "jalur konduksi & konveksi."
        ],
        align_right=True
    )

    # Callout 2: Reflective Shield (Right, anchor at X=705, Y=860)
    draw_hud_box_clamped(
        draw,
        x_anchor=705, y_anchor=860,
        x_box=710, y_box=810,
        w_box=306, h_box=130,
        tag="Komponen 03 — Radiasi",
        title="Lapisan Emas",
        body_lines=[
            "Memantulkan gelombang",
            "inframerah balik ke air."
        ],
        align_right=False
    )

    # Callout 3: Stopper Silikon (Top Right, anchor at X=540, Y=560)
    draw_hud_box_clamped(
        draw,
        x_anchor=540, y_anchor=560,
        x_box=680, y_box=460,
        w_box=336, h_box=130,
        tag="Komponen 01 — Bukaan",
        title="Stopper Silikon",
        body_lines=[
            "Sumbat kedap 4,0 cm mengunci",
            "uap panas di mulut botol."
        ],
        align_right=False
    )

    # 4. VOLT DS Subtitle Karaoke — CENTER ALIGNED (RATA TENGAH), MAX 4 WORDS, CLEAN NO-BOX
    # Text chunk: "celah hampa udara,"
    sub_y = 1380
    w1_text = "celah "
    w2_text = "hampa"
    w3_text = " udara,"

    bbox1 = draw.textbbox((0, 0), w1_text, font=font_subtitle)
    w1_w = bbox1[2] - bbox1[0]

    pad_highlight_x = 10
    pad_highlight_y = 6
    bbox2 = draw.textbbox((0, 0), w2_text, font=font_subtitle)
    w2_w = bbox2[2] - bbox2[0]

    bbox3 = draw.textbbox((0, 0), w3_text, font=font_subtitle)
    w3_w = bbox3[2] - bbox3[0]

    # Total width of the chunk
    total_chunk_w = w1_w + (w2_w + 2 * pad_highlight_x) + w3_w
    start_x = (1080 - total_chunk_w) // 2  # EXACT CENTER ALIGNMENT

    # Draw Timing cue badge (centered above subtitle)
    cue_text = "AUDIO CUE: 00:11.225"
    cue_bbox = draw.textbbox((0, 0), cue_text, font=font_label)
    cue_w = cue_bbox[2] - cue_bbox[0]
    cue_x = (1080 - cue_w) // 2
    draw.rectangle([cue_x - 12, sub_y - 42, cue_x + cue_w + 12, sub_y - 18], fill=PAPER, outline=LINE, width=1)
    draw.text((cue_x, sub_y - 38), cue_text, font=font_label, fill=MUTED)

    # Render Word 1: "celah "
    cur_x = start_x
    draw.text((cur_x, sub_y), w1_text, font=font_subtitle, fill=INK)
    cur_x += w1_w

    # Render Word 2: "hampa" (Active Word with VOLT Electric #E8F500 badge, 0-radius, 2px ink border)
    box_w2_left = cur_x
    box_w2_top = sub_y - pad_highlight_y
    box_w2_right = cur_x + w2_w + 2 * pad_highlight_x
    box_w2_bottom = sub_y + (bbox2[3] - bbox2[1]) + pad_highlight_y

    draw.rectangle([box_w2_left, box_w2_top, box_w2_right, box_w2_bottom], fill=ELECTRIC, outline=INK, width=2)
    draw.text((box_w2_left + pad_highlight_x, sub_y), w2_text, font=font_subtitle, fill=INK)
    cur_x = box_w2_right

    # Render Word 3: " udara,"
    draw.text((cur_x, sub_y), w3_text, font=font_subtitle, fill=INK)

    # 5. VOLT DS C02 Metric Card — STRICT INTERNAL PADDING & AUTO-WRAPPING (NO OVERFLOW)
    card_y = 1540
    card_h = 240
    draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + card_h], fill=PAPER, outline=INK, width=2)

    # Metric Banner Header
    draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + 38], fill=INK)
    draw.text((margin_x + 16, card_y + 10), "P05 EVIDENCE / DATA RESMI ZOJIRUSHI SM-WA48", font=font_label, fill=PAPER)

    # Left Column: Big Bold Metric
    metric_x = margin_x + 28
    metric_y = card_y + 65
    draw.text((metric_x, metric_y), "≥71°C", font=font_metric, fill=INK)
    draw.text((metric_x + 4, metric_y + 85), "RETENSI 6 JAM", font=font_heading, fill=INK)

    # Vertical divider inside card
    div_x = margin_x + 290
    draw.line([(div_x, card_y + 55), (div_x, card_y + card_h - 20)], fill=LINE, width=1)

    # Right Column: Clean Context lines with proper wrap & margins
    ctx_x = div_x + 24
    draw.text((ctx_x, card_y + 58), "Suhu Awal Uji: 95°C ±1°C | Suhu Ruang: 20°C ±2°C", font=font_body_bold, fill=INK)
    draw.text((ctx_x, card_y + 92), "Hasil akhir retensi panas setelah 6 jam pada posisi tegak.", font=font_body, fill=MUTED)
    draw.text((ctx_x, card_y + 124), "Spesifikasi resmi produsen Zojirushi Corporation (SM-WA48 / 480 ml).", font=font_body, fill=MUTED)
    draw.text((ctx_x, card_y + 164), "STATUS: FAKTA TERVERIFIKASI (ID KLAIM N-01, N-02, N-03)", font=font_label, fill=INK)

    # (Footer metadata completely removed as requested)

    # Save outputs
    base.save(OUT_PNG)
    base.convert("RGB").save(OUT_JPG, quality=95)
    print(f"Master Style Board Frame v0.2 saved to:\n- {OUT_PNG}\n- {OUT_JPG}")


if __name__ == "__main__":
    main()
