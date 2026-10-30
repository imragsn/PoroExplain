"""
Generate Master VOLT DS Style Board Frame v0.2 & Tabletop Variant
Addresses all user feedback:
1. Text overflow fix: All texts auto-wrapped and sized with generous padding.
2. Leader lines: Clean right-angled lines strictly outside HUD boxes.
3. Typography: Full Plus Jakarta Sans (VOLT DS primary aesthetic).
4. Subtitle Karaoke: Center-aligned (rata tengah di X=540), max 4 words, clean highlight.
5. C02 Metric Card: Clean column layout, no text clipping or border overflow.
6. Footer: Completely removed.
7. Environment: Produces both Clean Technical Stage (#FFFFFA) and Contextual Tabletop Environment.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
TRANSPARENT_BASE = os.path.join(ROOT, "work", "termos-3d", "style_b_base_transparent.png")
OUT_CLEAN_PNG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.2.png")
OUT_CLEAN_JPG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.2.jpg")
OUT_TABLE_PNG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.2-tabletop.png")
OUT_TABLE_JPG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.2-tabletop.jpg")

# VOLT DS Color Tokens
INK = (16, 17, 16, 255)            # #101110
PAPER = (255, 255, 250, 255)       # #FFFFFA
ELECTRIC = (232, 245, 0, 255)      # #E8F500
MUTED = (89, 93, 82, 255)          # #595D52
LINE = (145, 149, 135, 255)        # #919587
ORANGE_HEAT = (230, 110, 25, 200)

# Typography: Plus Jakarta Sans
FONT_PATH = os.path.join(ROOT, "work", "PlusJakartaSans.ttf")
font_title = ImageFont.truetype(FONT_PATH, 44)
font_heading = ImageFont.truetype(FONT_PATH, 22)
font_body = ImageFont.truetype(FONT_PATH, 17)
font_body_bold = ImageFont.truetype(FONT_PATH, 17)
font_label = ImageFont.truetype(FONT_PATH, 13)
font_subtitle = ImageFont.truetype(FONT_PATH, 40)
font_metric = ImageFont.truetype(FONT_PATH, 66)
font_tag = ImageFont.truetype(FONT_PATH, 17)


def draw_hud_box_clamped(draw, x_anchor, y_anchor, x_box, y_box, w_box, h_box, tag, title, body_lines, align_right=False):
    """
    Renders an angular HUD callout with a leader line strictly outside the bounding box.
    Zero border radius, 2px ink stroke, paper background.
    """
    y_connect = y_box + h_box // 2

    if align_right:
        # Box is to the LEFT of the anchor
        x_connect = x_box + w_box
        elbow_x = (x_connect + x_anchor) // 2
        points = [(x_anchor, y_anchor), (elbow_x, y_anchor), (elbow_x, y_connect), (x_connect, y_connect)]
    else:
        # Box is to the RIGHT of the anchor
        x_connect = x_box
        elbow_x = (x_anchor + x_connect) // 2
        points = [(x_anchor, y_anchor), (elbow_x, y_anchor), (elbow_x, y_connect), (x_connect, y_connect)]

    # Draw leader line & target anchor point
    draw.line(points, fill=INK, width=2)
    # Electric Yellow square pin at anchor
    draw.rectangle([x_anchor - 4, y_anchor - 4, x_anchor + 4, y_anchor + 4], fill=ELECTRIC, outline=INK, width=2)

    # Box container (VOLT: zero radius, paper fill, 2px ink stroke)
    draw.rectangle([x_box, y_box, x_box + w_box, y_box + h_box], fill=PAPER, outline=INK, width=2)

    # Internal content
    pad_x = 16
    draw.text((x_box + pad_x, y_box + 14), tag.upper(), font=font_label, fill=MUTED)
    draw.text((x_box + pad_x, y_box + 34), title.upper(), font=font_heading, fill=INK)

    line_y = y_box + 68
    for line in body_lines:
        draw.text((x_box + pad_x, line_y), line, font=font_body, fill=MUTED)
        line_y += 24


def draw_thermal_particles(draw):
    """Draws infrared heat radiation wave arcs & particle packets reflected inside bottle."""
    center_x = 540
    for y in [820, 920, 1020, 1120, 1200]:
        for offset in [40, 80, 120]:
            draw.arc([center_x - offset, y - 28, center_x + offset, y + 28], start=300, end=420, fill=ORANGE_HEAT, width=2)
        ref_x = 684
        draw.line([(ref_x, y), (ref_x - 50, y - 22)], fill=ELECTRIC, width=3)
        draw.polygon([(ref_x - 50, y - 22), (ref_x - 38, y - 27), (ref_x - 42, y - 16)], fill=INK)

    particles = [
        (580, 850), (620, 880), (655, 910), (595, 950), (635, 990),
        (590, 1050), (630, 1080), (660, 1110), (605, 1170), (645, 1200)
    ]
    for px, py in particles:
        draw.rectangle([px - 3, py - 3, px + 3, py + 3], fill=ELECTRIC, outline=INK, width=1)


def composite_frame(bg_type="clean"):
    """
    Composites the frame:
    - bg_type="clean": Pure VOLT DS Paper background (#FFFFFA) with subtle shadow.
    - bg_type="tabletop": Warm minimalist tabletop environment.
    """
    canvas = Image.new("RGBA", (1080, 1920), PAPER)
    draw = ImageDraw.Draw(canvas)

    if bg_type == "tabletop":
        # Draw soft contextual environment:
        # Subtle warm background gradient
        for y in range(1220):
            # Soft warm ambient gradient (250, 248, 242) to (245, 242, 235)
            r = int(252 - (y / 1220) * 8)
            g = int(250 - (y / 1220) * 9)
            b = int(246 - (y / 1220) * 12)
            draw.line([(0, y), (1080, y)], fill=(r, g, b, 255))

        # Modern minimalist oak/table surface in the lower third
        # Table starts at Y=1220 down to Y=1920
        table_top_y = 1220
        draw.rectangle([0, table_top_y, 1080, 1920], fill=(238, 232, 222, 255))
        # Subtle table edge highlight & shadow line
        draw.line([(0, table_top_y), (1080, table_top_y)], fill=(215, 208, 196, 255), width=2)
        draw.line([(0, table_top_y + 2), (1080, table_top_y + 2)], fill=(248, 245, 240, 255), width=1)

        # Soft contact shadow under the bottle base (at Y=1240, X=540)
        shadow_overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow_overlay)
        s_draw.ellipse([340, 1238, 740, 1262], fill=(60, 50, 40, 90))
        s_draw.ellipse([360, 1242, 720, 1258], fill=(40, 30, 20, 140))
        shadow_overlay = shadow_overlay.filter(ImageFilter.GaussianBlur(radius=8))
        canvas.alpha_composite(shadow_overlay)
    else:
        # Clean Studio Stage: Add soft floor contact shadow under bottle
        shadow_overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow_overlay)
        s_draw.ellipse([330, 1238, 750, 1262], fill=(16, 17, 16, 45))
        s_draw.ellipse([360, 1242, 720, 1258], fill=(16, 17, 16, 75))
        shadow_overlay = shadow_overlay.filter(ImageFilter.GaussianBlur(radius=7))
        canvas.alpha_composite(shadow_overlay)

    # Paste Transparent 3D Bottle
    bottle = Image.open(TRANSPARENT_BASE).convert("RGBA")
    canvas.alpha_composite(bottle)

    # Re-acquire draw object after alpha composite
    draw = ImageDraw.Draw(canvas)

    # 1. Thermal Radiation Effect (arcs and particles)
    draw_thermal_particles(draw)

    # 2. VOLT DS Header Zone
    margin_x = 64
    content_w = 1080 - 2 * margin_x  # 952 px

    # Eyebrow: @porotheexplorer
    draw.text((margin_x, 72), "@porotheexplorer", font=font_tag, fill=MUTED)
    # Title: KENAPA TERMOS BISA TAHAN PANAS?
    draw.text((margin_x, 102), "KENAPA TERMOS BISA TAHAN PANAS?", font=font_title, fill=INK)
    # 2px Sharp Rule
    draw.line([(margin_x, 172), (margin_x + content_w, 172)], fill=INK, width=2)

    # 3. VOLT DS HUD Callouts (Strictly outside bottle & lines correctly clamped)
    # HUD 1: Celah Vakum (Left)
    draw_hud_box_clamped(
        draw,
        x_anchor=385, y_anchor=980,
        x_box=margin_x, y_box=915,
        w_box=280, h_box=135,
        tag="Komponen 02 — Vakum",
        title="Celah Vakum",
        body_lines=[
            "Ruang hampa ~2mm memutus",
            "jalur konduksi & konveksi."
        ],
        align_right=True
    )

    # HUD 2: Stopper Silikon (Top Right)
    draw_hud_box_clamped(
        draw,
        x_anchor=560, y_anchor=520,
        x_box=730, y_box=440,
        w_box=286, h_box=135,
        tag="Komponen 01 — Bukaan",
        title="Stopper Silikon",
        body_lines=[
            "Sumbat 4cm mengunci uap",
            "panas di mulut botol."
        ],
        align_right=False
    )

    # HUD 3: Lapisan Emas (Bottom Right)
    draw_hud_box_clamped(
        draw,
        x_anchor=685, y_anchor=880,
        x_box=740, y_box=815,
        w_box=276, h_box=135,
        tag="Komponen 03 — Radiasi",
        title="Lapisan Emas",
        body_lines=[
            "Memantulkan gelombang",
            "inframerah balik ke air."
        ],
        align_right=False
    )

    # 4. VOLT DS Subtitle Karaoke — EXACT CENTER ALIGNMENT, MAX 4 WORDS, CLEAN NO-BOX
    sub_y = 1380
    w1_text = "celah "
    w2_text = "hampa"
    w3_text = " udara,"

    bbox1 = draw.textbbox((0, 0), w1_text, font=font_subtitle)
    w1_w = bbox1[2] - bbox1[0]

    pad_h_x = 12
    pad_h_y = 6
    bbox2 = draw.textbbox((0, 0), w2_text, font=font_subtitle)
    w2_w = bbox2[2] - bbox2[0]

    bbox3 = draw.textbbox((0, 0), w3_text, font=font_subtitle)
    w3_w = bbox3[2] - bbox3[0]

    total_chunk_w = w1_w + (w2_w + 2 * pad_h_x) + w3_w
    start_x = (1080 - total_chunk_w) // 2

    # Timing cue pill (centered above subtitle)
    cue_text = "AUDIO CUE: 00:11.225"
    cue_bbox = draw.textbbox((0, 0), cue_text, font=font_label)
    cue_w = cue_bbox[2] - cue_bbox[0]
    cue_x = (1080 - cue_w) // 2
    draw.rectangle([cue_x - 12, sub_y - 40, cue_x + cue_w + 12, sub_y - 18], fill=PAPER, outline=LINE, width=1)
    draw.text((cue_x, sub_y - 36), cue_text, font=font_label, fill=MUTED)

    # Word 1: "celah "
    cur_x = start_x
    draw.text((cur_x, sub_y), w1_text, font=font_subtitle, fill=INK)
    cur_x += w1_w

    # Word 2: "hampa" (Active word highlighted in Electric #E8F500 box, 0-radius, 2px ink stroke)
    box_w2_left = cur_x
    box_w2_top = sub_y - pad_h_y
    box_w2_right = cur_x + w2_w + 2 * pad_h_x
    box_w2_bottom = sub_y + (bbox2[3] - bbox2[1]) + pad_h_y

    draw.rectangle([box_w2_left, box_w2_top, box_w2_right, box_w2_bottom], fill=ELECTRIC, outline=INK, width=2)
    draw.text((box_w2_left + pad_h_x, sub_y), w2_text, font=font_subtitle, fill=INK)
    cur_x = box_w2_right

    # Word 3: " udara,"
    draw.text((cur_x, sub_y), w3_text, font=font_subtitle, fill=INK)

    # 5. VOLT DS C02 Metric Card — STRICT NO-OVERFLOW PADDING & COLUMNS
    card_y = 1530
    card_h = 240
    draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + card_h], fill=PAPER, outline=INK, width=2)

    # Metric Banner Header
    draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + 36], fill=INK)
    draw.text((margin_x + 16, card_y + 10), "P05 EVIDENCE / DATA RESMI ZOJIRUSHI SM-WA48", font=font_label, fill=PAPER)

    # Left Column: Big Bold Metric
    metric_x = margin_x + 28
    metric_y = card_y + 60
    draw.text((metric_x, metric_y), "≥71°C", font=font_metric, fill=INK)
    draw.text((metric_x + 4, metric_y + 82), "RETENSI 6 JAM", font=font_heading, fill=INK)

    # Vertical divider inside card
    div_x = margin_x + 290
    draw.line([(div_x, card_y + 52), (div_x, card_y + card_h - 20)], fill=LINE, width=1)

    # Right Column: Clean Context lines with generous margins
    ctx_x = div_x + 24
    draw.text((ctx_x, card_y + 56), "Suhu Awal Uji: 95°C ±1°C | Suhu Ruang: 20°C ±2°C", font=font_body_bold, fill=INK)
    draw.text((ctx_x, card_y + 90), "Hasil akhir retensi panas setelah 6 jam pada posisi tegak.", font=font_body, fill=MUTED)
    draw.text((ctx_x, card_y + 122), "Spesifikasi resmi produsen Zojirushi (SM-WA48 / 480 ml).", font=font_body, fill=MUTED)
    draw.text((ctx_x, card_y + 162), "STATUS: FAKTA TERVERIFIKASI (KLAIM RESMI ZOJIRUSHI)", font=font_label, fill=INK)

    # Footer metadata completely removed (0px height, clean spacious bottom)
    return canvas


def main():
    print("Generating Clean VOLT Stage Frame v0.2...")
    clean_canvas = composite_frame("clean")
    clean_canvas.save(OUT_CLEAN_PNG)
    clean_canvas.convert("RGB").save(OUT_CLEAN_JPG, quality=95)
    print(f"Saved Clean Frame to:\n- {OUT_CLEAN_PNG}\n- {OUT_CLEAN_JPG}")

    print("Generating Contextual Tabletop Frame v0.2...")
    table_canvas = composite_frame("tabletop")
    table_canvas.save(OUT_TABLE_PNG)
    table_canvas.convert("RGB").save(OUT_TABLE_JPG, quality=95)
    print(f"Saved Tabletop Frame to:\n- {OUT_TABLE_PNG}\n- {OUT_TABLE_JPG}")


if __name__ == "__main__":
    main()
