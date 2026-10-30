"""
Generate Master Style Board Frame v0.3
Integrates all latest feedback:
1. Locked Positions: Bottle centered, HUD boxes, Subtitle at X=540, Y=1380, Metric card at Y=1530.
2. Space Grotesk Typography: Proportional combinations of Regular (400), Medium (500), SemiBold (600), Bold (700), and synthetic Italic for key numbers.
3. VOLT DS index.html Semantic Color System:
   - Positive Green (#235E42) for Stopper Silikon & Verified Status
   - Info Blue (#235A87) for Celah Vakum (physics isolation)
   - Thermal Amber (#B76E00) for Lapisan Emas (infrared reflection)
   - Wash Tint (#F7FACD) for Metric block accent & cue badge
   - Electric Yellow (#E8F500) for Karaoke active word focus & anchor pins
4. Dual Render Comparison:
   - Clean Technical Stage (#FFFFFA)
   - Contextual Tabletop Environment (Minimalist warm desk + soft ambient depth)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
TRANSPARENT_BASE = os.path.join(ROOT, "work", "termos-3d", "style_b_base_transparent.png")
FONT_PATH = os.path.join(ROOT, "work", "fonts", "SpaceGrotesk-VariableFont_wght.ttf")

OUT_CLEAN_PNG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.3-clean.png")
OUT_CLEAN_JPG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.3-clean.jpg")
OUT_TABLE_PNG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.3-tabletop.png")
OUT_TABLE_JPG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.3-tabletop.jpg")

# Mirror update for v0.2 files
OUT_V02_PNG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.2.png")
OUT_V02_JPG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.2.jpg")

# VOLT DS Color Tokens (exact from index.html & tokens.json)
INK = (16, 17, 16, 255)            # #101110
PAPER = (255, 255, 250, 255)       # #FFFFFA
ELECTRIC = (232, 245, 0, 255)      # #E8F500
WASH = (247, 250, 205, 255)        # #F7FACD
MUTED = (89, 93, 82, 255)          # #595D52
LINE = (145, 149, 135, 255)        # #919587
POSITIVE = (35, 94, 66, 255)       # #235E42
INFO = (35, 90, 135, 255)          # #235A87
AMBER = (183, 110, 0, 255)         # #B76E00 / #755000
HEAT_ORANGE = (230, 110, 25, 210)


def get_font(size, weight=400):
    f = ImageFont.truetype(FONT_PATH, size)
    f.set_variation_by_axes([weight])
    return f


font_title = get_font(44, 700)
font_eyebrow = get_font(16, 600)
font_heading = get_font(21, 700)
font_body = get_font(16, 400)
font_body_bold = get_font(16, 700)
font_tag = get_font(12, 700)
font_subtitle = get_font(40, 400)
font_subtitle_bold = get_font(40, 700)
font_metric_big = get_font(66, 700)
font_metric_label = get_font(20, 700)
font_badge = get_font(12, 700)


def draw_hud_box_semantic(draw, x_anchor, y_anchor, x_box, y_box, w_box, h_box, tag, title, body_lines, accent_color, align_right=False):
    """
    Renders an angular HUD callout with:
    - Dedicated semantic header strip (accent color)
    - 2px Ink stroke, 0-radius
    - Leader line strictly outside box
    - Anchor pinpoint with accent fill
    """
    y_connect = y_box + h_box // 2

    if align_right:
        # Box is to the LEFT of anchor
        x_connect = x_box + w_box
        elbow_x = (x_connect + x_anchor) // 2
        points = [(x_anchor, y_anchor), (elbow_x, y_anchor), (elbow_x, y_connect), (x_connect, y_connect)]
    else:
        # Box is to the RIGHT of anchor
        x_connect = x_box
        elbow_x = (x_anchor + x_connect) // 2
        points = [(x_anchor, y_anchor), (elbow_x, y_anchor), (elbow_x, y_connect), (x_connect, y_connect)]

    # Draw leader line
    draw.line(points, fill=INK, width=2)
    # Anchor pinpoint (Square 8x8 with accent color & 2px ink outline)
    draw.rectangle([x_anchor - 4, y_anchor - 4, x_anchor + 4, y_anchor + 4], fill=accent_color, outline=INK, width=2)

    # Box background (Paper #FFFFFA) & 2px Ink outline
    draw.rectangle([x_box, y_box, x_box + w_box, y_box + h_box], fill=PAPER, outline=INK, width=2)

    # Semantic Header Strip (VOLT DS index.html style)
    header_h = 26
    draw.rectangle([x_box, y_box, x_box + w_box, y_box + header_h], fill=accent_color)
    draw.text((x_box + 14, y_box + 6), tag.upper(), font=font_tag, fill=PAPER)

    # Box Title (Bold 700 Space Grotesk)
    pad_x = 16
    draw.text((x_box + pad_x, y_box + 38), title.upper(), font=font_heading, fill=INK)

    # Body lines (Regular 400 with comfortable line height)
    line_y = y_box + 74
    for line in body_lines:
        draw.text((x_box + pad_x, line_y), line, font=font_body, fill=MUTED)
        line_y += 24


def draw_thermal_particles(draw):
    """Draws infrared heat radiation wave arcs & particle packets reflected inside bottle."""
    center_x = 540
    for y in [820, 920, 1020, 1120, 1200]:
        for offset in [40, 80, 120]:
            draw.arc([center_x - offset, y - 28, center_x + offset, y + 28], start=300, end=420, fill=HEAT_ORANGE, width=2)
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
    canvas = Image.new("RGBA", (1080, 1920), PAPER)
    draw = ImageDraw.Draw(canvas)

    if bg_type == "tabletop":
        # Warm minimalist studio environment
        for y in range(1220):
            r = int(252 - (y / 1220) * 8)
            g = int(250 - (y / 1220) * 9)
            b = int(246 - (y / 1220) * 12)
            draw.line([(0, y), (1080, y)], fill=(r, g, b, 255))

        table_top_y = 1220
        draw.rectangle([0, table_top_y, 1080, 1920], fill=(238, 232, 222, 255))
        draw.line([(0, table_top_y), (1080, table_top_y)], fill=(215, 208, 196, 255), width=2)
        draw.line([(0, table_top_y + 2), (1080, table_top_y + 2)], fill=(248, 245, 240, 255), width=1)

        shadow_overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow_overlay)
        s_draw.ellipse([340, 1238, 740, 1262], fill=(60, 50, 40, 90))
        s_draw.ellipse([360, 1242, 720, 1258], fill=(40, 30, 20, 140))
        shadow_overlay = shadow_overlay.filter(ImageFilter.GaussianBlur(radius=8))
        canvas.alpha_composite(shadow_overlay)
    else:
        # Clean Technical Stage with soft floor shadow
        shadow_overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow_overlay)
        s_draw.ellipse([330, 1238, 750, 1262], fill=(16, 17, 16, 45))
        s_draw.ellipse([360, 1242, 720, 1258], fill=(16, 17, 16, 75))
        shadow_overlay = shadow_overlay.filter(ImageFilter.GaussianBlur(radius=7))
        canvas.alpha_composite(shadow_overlay)

    # Paste Transparent 3D Model
    bottle = Image.open(TRANSPARENT_BASE).convert("RGBA")
    canvas.alpha_composite(bottle)
    draw = ImageDraw.Draw(canvas)

    # 1. Thermal Radiation Effect
    draw_thermal_particles(draw)

    # 2. Header Zone (Locked positions)
    margin_x = 64
    content_w = 1080 - 2 * margin_x  # 952 px

    # Eyebrow: @porotheexplorer with subtle electric pill accent
    draw.rectangle([margin_x, 70, margin_x + 160, 94], fill=WASH, outline=LINE, width=1)
    draw.text((margin_x + 10, 74), "@porotheexplorer", font=font_eyebrow, fill=INK)

    # Title: KENAPA TERMOS BISA TAHAN PANAS? in Space Grotesk Bold 700
    draw.text((margin_x, 106), "KENAPA TERMOS BISA TAHAN PANAS?", font=font_title, fill=INK)
    # 2px Sharp Rule
    draw.line([(margin_x, 174), (margin_x + content_w, 174)], fill=INK, width=2)

    # 3. HUD Callouts with Rich Semantic Colors (Positive Green, Info Blue, Amber)
    # HUD 1: Stopper Silikon (Top Right, Positive Green #235E42)
    draw_hud_box_semantic(
        draw,
        x_anchor=560, y_anchor=520,
        x_box=730, y_box=430,
        w_box=286, h_box=140,
        tag="01 / BUKAAN KEDAP",
        title="Stopper Silikon",
        body_lines=[
            "Sumbat 4,0 cm mengunci uap",
            "panas agar tidak konveksi."
        ],
        accent_color=POSITIVE,
        align_right=False
    )

    # HUD 2: Celah Vakum (Left, Info Blue #235A87)
    draw_hud_box_semantic(
        draw,
        x_anchor=385, y_anchor=980,
        x_box=margin_x, y_box=905,
        w_box=286, h_box=140,
        tag="02 / ISOLASI FISIKA",
        title="Celah Vakum",
        body_lines=[
            "Ruang hampa ~2mm memutus",
            "jalur konduksi & konveksi."
        ],
        accent_color=INFO,
        align_right=True
    )

    # HUD 3: Lapisan Emas (Bottom Right, Thermal Amber #B76E00)
    draw_hud_box_semantic(
        draw,
        x_anchor=685, y_anchor=880,
        x_box=740, y_box=810,
        w_box=276, h_box=140,
        tag="03 / RADIASI PANAS",
        title="Lapisan Emas",
        body_lines=[
            "Memantulkan gelombang",
            "inframerah balik ke air."
        ],
        accent_color=AMBER,
        align_right=False
    )

    # 4. Subtitle Karaoke (Locked at Y=1380, Center-Aligned at X=540)
    sub_y = 1380
    w1_text = "celah "
    w2_text = "hampa"
    w3_text = " udara,"

    bbox1 = draw.textbbox((0, 0), w1_text, font=font_subtitle)
    w1_w = bbox1[2] - bbox1[0]

    pad_h_x = 12
    pad_h_y = 6
    bbox2 = draw.textbbox((0, 0), w2_text, font=font_subtitle_bold)
    w2_w = bbox2[2] - bbox2[0]

    bbox3 = draw.textbbox((0, 0), w3_text, font=font_subtitle)
    w3_w = bbox3[2] - bbox3[0]

    total_chunk_w = w1_w + (w2_w + 2 * pad_h_x) + w3_w
    start_x = (1080 - total_chunk_w) // 2

    # Audio cue badge (Wash #F7FACD fill, Line border, centered above)
    cue_text = "AUDIO CUE: 00:11.225"
    cue_bbox = draw.textbbox((0, 0), cue_text, font=font_tag)
    cue_w = cue_bbox[2] - cue_bbox[0]
    cue_x = (1080 - cue_w) // 2
    draw.rectangle([cue_x - 12, sub_y - 42, cue_x + cue_w + 12, sub_y - 18], fill=WASH, outline=LINE, width=1)
    draw.text((cue_x, sub_y - 38), cue_text, font=font_tag, fill=INK)

    # Subtitle word 1
    cur_x = start_x
    draw.text((cur_x, sub_y), w1_text, font=font_subtitle, fill=INK)
    cur_x += w1_w

    # Subtitle active word (Electric Yellow #E8F500 box, 0-radius, 2px ink stroke, Bold 700)
    box_w2_left = cur_x
    box_w2_top = sub_y - pad_h_y
    box_w2_right = cur_x + w2_w + 2 * pad_h_x
    box_w2_bottom = sub_y + (bbox2[3] - bbox2[1]) + pad_h_y

    draw.rectangle([box_w2_left, box_w2_top, box_w2_right, box_w2_bottom], fill=ELECTRIC, outline=INK, width=2)
    draw.text((box_w2_left + pad_h_x, sub_y), w2_text, font=font_subtitle_bold, fill=INK)
    cur_x = box_w2_right

    # Subtitle word 3
    draw.text((cur_x, sub_y), w3_text, font=font_subtitle, fill=INK)

    # 5. VOLT DS Metric Evidence Card (Locked at Y=1530)
    card_y = 1530
    card_h = 245
    # Card outer border 2px Ink
    draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + card_h], fill=PAPER, outline=INK, width=2)

    # Dark Banner Header
    draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + 36], fill=INK)
    draw.text((margin_x + 16, card_y + 10), "P05 EVIDENCE / DATA RESMI ZOJIRUSHI CORPORATION", font=font_tag, fill=PAPER)

    # Left Column: Highlighted in Soft Wash Tint (#F7FACD) for high-attention emphasis
    div_x = margin_x + 295
    draw.rectangle([margin_x, card_y + 36, div_x, card_y + card_h], fill=WASH)
    draw.line([(div_x, card_y + 36), (div_x, card_y + card_h)], fill=INK, width=2)

    metric_x = margin_x + 28
    metric_y = card_y + 54
    draw.text((metric_x, metric_y), "≥71°C", font=font_metric_big, fill=INK)
    draw.text((metric_x + 4, metric_y + 80), "RETENSI 6 JAM", font=font_metric_label, fill=INK)
    draw.text((metric_x + 4, metric_y + 112), "Suhu Cairan Minimum", font=font_tag, fill=MUTED)

    # Right Column: Clean White with Context lines & Positive Status Badge
    ctx_x = div_x + 24
    draw.text((ctx_x, card_y + 54), "Suhu Awal Uji: 95°C ±1°C | Suhu Ruang: 20°C ±2°C", font=font_body_bold, fill=INK)
    draw.text((ctx_x, card_y + 88), "Hasil akhir retensi panas setelah 6 jam pada posisi tegak.", font=font_body, fill=MUTED)
    draw.text((ctx_x, card_y + 118), "Spesifikasi resmi produsen Zojirushi Corporation (SM-WA48 / 480 ml).", font=font_body, fill=MUTED)

    # Verified Status Pill in Positive Green #235E42 (0-radius)
    pill_w = 345
    pill_h = 28
    pill_y = card_y + 154
    draw.rectangle([ctx_x, pill_y, ctx_x + pill_w, pill_y + pill_h], fill=POSITIVE)
    draw.text((ctx_x + 14, pill_y + 6), "STATUS: FAKTA TERVERIFIKASI (KLAIM RESMI)", font=font_badge, fill=PAPER)

    # Standard badge in Info Blue beside it
    badge2_x = ctx_x + pill_w + 12
    badge2_w = 120
    draw.rectangle([badge2_x, pill_y, badge2_x + badge2_w, pill_y + pill_h], fill=INFO)
    draw.text((badge2_x + 12, pill_y + 6), "STANDAR JIS", font=font_badge, fill=PAPER)

    # Negative space bottom (clean zero-height footer)
    return canvas


def main():
    print("Generating Clean VOLT Stage Frame v0.3...")
    clean_canvas = composite_frame("clean")
    clean_canvas.save(OUT_CLEAN_PNG)
    clean_canvas.convert("RGB").save(OUT_CLEAN_JPG, quality=95)
    # Also update v0.2 files
    clean_canvas.save(OUT_V02_PNG)
    clean_canvas.convert("RGB").save(OUT_V02_JPG, quality=95)
    print(f"Saved Clean Frame to:\n- {OUT_CLEAN_PNG}\n- {OUT_CLEAN_JPG}")

    print("Generating Contextual Tabletop Frame v0.3...")
    table_canvas = composite_frame("tabletop")
    table_canvas.save(OUT_TABLE_PNG)
    table_canvas.convert("RGB").save(OUT_TABLE_JPG, quality=95)
    print(f"Saved Tabletop Frame to:\n- {OUT_TABLE_PNG}\n- {OUT_TABLE_JPG}")


if __name__ == "__main__":
    main()
