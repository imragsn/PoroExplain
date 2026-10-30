"""
Composite VOLT DS Style Board Frame
Renders 1 master style frame (1080x1920) incorporating:
- Style B 3D Cel-Shaded Render with Freestyle ink outlines
- Thermal radiation particle wave graphics
- VOLT DS Header, Typography, and 2px Ink Rules
- VOLT DS Technical Annotation HUDs with 0-radius angular leader lines
- Clean Subtitle Chunk (<= 4 words) with Electric Yellow (#E8F500) active word highlight
- VOLT DS C02 Metric Card (6-hour retention >=71°C)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
BASE_IMG = os.path.join(ROOT, "work", "termos-3d", "style_b_base_1080x1920.png")
OUT_PNG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.1.png")
OUT_JPG = os.path.join(ROOT, "outputs", "termos-05-style-frame-v0.1.jpg")

# VOLT DS Color Tokens
INK = (16, 17, 16, 255)            # #101110
PAPER = (255, 255, 250, 255)       # #FFFFFA
ELECTRIC = (232, 245, 0, 255)      # #E8F500 (Acid Electric Yellow)
WASH = (247, 250, 205, 255)        # #F7FACD
MUTED = (89, 93, 82, 255)          # #595D52
LINE = (145, 149, 135, 255)        # #919587
AMBER_HOT = (230, 126, 34, 255)    # Heat radiation amber
GOLD_SHIELD = (245, 183, 0, 255)   # Foil reflection

# Load Fonts
FONT_DIR = r"C:\Windows\Fonts"
font_title = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 48)
font_heading = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 30)
font_body = ImageFont.truetype(os.path.join(FONT_DIR, "arial.ttf"), 22)
font_body_bold = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 22)
font_label = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 16)
font_subtitle = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 44)
font_metric = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 72)
font_tag = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 18)


def draw_hud_box(draw, x_anchor, y_anchor, x_box, y_box, w_box, h_box, tag, title, body, align_right=False):
    # 2px Sharp Angular Leader Line (Zero Radius)
    # Line starts at anchor on 3D object, bends at 45/90 deg, lands on box edge
    if align_right:
        # Box is to the left of the anchor
        x_connect = x_box + w_box
        y_connect = y_box + h_box // 2
        elbow_x = x_anchor - 40
        points = [(x_anchor, y_anchor), (elbow_x, y_anchor), (elbow_x, y_connect), (x_connect, y_connect)]
    else:
        # Box is to the right of the anchor
        x_connect = x_box
        y_connect = y_box + h_box // 2
        elbow_x = x_anchor + 40
        points = [(x_anchor, y_anchor), (elbow_x, y_anchor), (elbow_x, y_connect), (x_connect, y_connect)]
        
    draw.line(points, fill=INK, width=2)
    # Anchor target dot
    draw.rectangle([x_anchor - 4, y_anchor - 4, x_anchor + 4, y_anchor + 4], fill=ELECTRIC, outline=INK, width=2)

    # Sharp Technical Panel Box (VOLT: zero radius, 2px ink stroke, paper fill)
    draw.rectangle([x_box, y_box, x_box + w_box, y_box + h_box], fill=PAPER, outline=INK, width=2)
    
    # Tag
    draw.text((x_box + 16, y_box + 14), tag.upper(), font=font_label, fill=MUTED)
    # Title
    draw.text((x_box + 16, y_box + 38), title.upper(), font=font_heading, fill=INK)
    # Body
    draw.text((x_box + 16, y_box + 76), body, font=font_body, fill=MUTED)


def draw_thermal_particles(draw):
    # Conceptual Thermal Radiation Wave Arcs and Particles reflecting off the inner wall
    center_x = 540
    # Radiation emanating from hot liquid core (Y=800 to Y=1250)
    for y in [820, 920, 1020, 1120, 1220]:
        # Outgoing radiation waves towards right wall (gold reflective layer at X=705)
        for offset in [40, 80, 120]:
            draw.arc([center_x - offset, y - 30, center_x + offset, y + 30], start=300, end=420, fill=(230, 126, 34, 180), width=2)
        
        # Bounced reflection arrow returning inward from gold reflective layer
        ref_x = 698
        draw.line([(ref_x, y), (ref_x - 55, y - 25)], fill=ELECTRIC, width=3)
        # Arrowhead pointing inward
        draw.polygon([(ref_x - 55, y - 25), (ref_x - 42, y - 30), (ref_x - 47, y - 18)], fill=INK)

    # Radiant particle dots
    particle_coords = [
        (580, 850), (620, 880), (660, 910), (600, 950), (640, 990),
        (590, 1050), (630, 1080), (665, 1110), (610, 1180), (650, 1210)
    ]
    for px, py in particle_coords:
        draw.rectangle([px - 3, py - 3, px + 3, py + 3], fill=ELECTRIC, outline=INK, width=1)


def main():
    base = Image.open(BASE_IMG).convert("RGBA")
    draw = ImageDraw.Draw(base)

    # 1. Thermal Radiation Effect (Gelombang Partikel & Pantulan)
    draw_thermal_particles(draw)

    # 2. VOLT DS Header Zone (Top, Y=70 to Y=220)
    margin_x = 64
    content_w = 1080 - 2 * margin_x  # 952 px

    # Eyebrow / Tag
    draw.text((margin_x, 70), "01 / VOLT SYSTEM — MEKANISME TERMAL", font=font_tag, fill=MUTED)
    # Title
    draw.text((margin_x, 102), "KENAPA TERMOS BISA TAHAN PANAS?", font=font_title, fill=INK)
    # Subhead / Context
    draw.text((margin_x, 168), "Bedah 5 lapisan fisik penahan konduksi, konveksi, dan radiasi termal.", font=font_body, fill=MUTED)
    # 2px Sharp Rule
    draw.line([(margin_x, 210), (margin_x + content_w, 210)], fill=INK, width=2)

    # 3. VOLT DS Technical Annotation HUDs (3 Key Callouts)
    # Callout 1: Vacuum Gap (Left, anchor at X=370, Y=980)
    draw_hud_box(
        draw,
        x_anchor=370, y_anchor=980,
        x_box=margin_x, y_box=910,
        w_box=310, h_box=120,
        tag="Komponen 02 — Vakum",
        title="Celah Vakum",
        body="Ruang hampa ~2mm memutus\njalur konduksi & konveksi.",
        align_right=True
    )

    # Callout 2: Reflective Shield (Right, anchor at X=705, Y=860)
    draw_hud_box(
        draw,
        x_anchor=705, y_anchor=860,
        x_box=720, y_box=810,
        w_box=296, h_box=120,
        tag="Komponen 03 — Radiasi",
        title="Lapisan Emas",
        body="Memantulkan gelombang\ninframerah balik ke air.",
        align_right=False
    )

    # Callout 3: Stopper Silikon (Top Right, anchor at X=540, Y=560)
    draw_hud_box(
        draw,
        x_anchor=540, y_anchor=560,
        x_box=680, y_box=460,
        w_box=336, h_box=120,
        tag="Komponen 01 — Bukaan",
        title="Stopper Silikon",
        body="Sumbat kedap 4,0 cm mengunci\nuap panas di mulut botol.",
        align_right=False
    )

    # 4. VOLT DS Subtitle Karaoke (Bottom Safe Zone, Y ≈ 1380 to 1480)
    # Rule: Max 4 words chunk, clean text without dark bubble container box!
    # Active Chunk: "celah hampa udara,"
    sub_y = 1390
    
    # Timing pill badge
    draw.rectangle([margin_x, sub_y - 36, margin_x + 230, sub_y - 12], fill=PAPER, outline=LINE, width=1)
    draw.text((margin_x + 10, sub_y - 32), "AUDIO CUE: 00:11.225", font=font_label, fill=MUTED)

    # Subtitle Words
    # Word 1: "celah" (Normal Ink)
    w1 = "celah "
    bbox1 = draw.textbbox((margin_x, sub_y), w1, font=font_subtitle)
    draw.text((margin_x, sub_y), w1, font=font_subtitle, fill=INK)

    # Word 2: "hampa" (ACTIVE WORD HIGHLIGHT in VOLT Electric #E8F500)
    # Sharp rectangular box, 2px ink stroke, zero radius!
    w2 = "hampa"
    w2_x = bbox1[2] + 4
    bbox2 = draw.textbbox((w2_x, sub_y), w2, font=font_subtitle)
    pad_x, pad_y = 10, 6
    draw.rectangle(
        [bbox2[0] - pad_x, bbox2[1] - pad_y, bbox2[2] + pad_x, bbox2[3] + pad_y],
        fill=ELECTRIC, outline=INK, width=2
    )
    draw.text((w2_x, sub_y), w2, font=font_subtitle, fill=INK)

    # Word 3: "udara," (Normal Ink)
    w3 = " udara,"
    w3_x = bbox2[2] + pad_x + 6
    draw.text((w3_x, sub_y), w3, font=font_subtitle, fill=INK)

    # Subtitle Context Label
    draw.text((margin_x, sub_y + 60), "Subtitle: Maksimal 4 kata per tayang, clean overlay tanpa kotak hitam.", font=font_body, fill=MUTED)

    # 5. VOLT DS C02 Metric Card (Bottom Evidence Zone, Y=1580 to 1840)
    card_y = 1580
    card_h = 220
    draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + card_h], fill=PAPER, outline=INK, width=2)
    
    # Metric Callout Header
    draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + 42], fill=INK)
    draw.text((margin_x + 16, card_y + 12), "P05 EVIDENCE / DATA RESMI ZOJIRUSHI SM-WA48", font=font_label, fill=PAPER)

    # Metric Number & Unit
    draw.text((margin_x + 24, card_y + 60), "≥71°C", font=font_metric, fill=INK)

    # Metric Details
    detail_x = margin_x + 280
    draw.text((detail_x, card_y + 64), "RETENSI PANAS 6 JAM", font=font_heading, fill=INK)
    draw.text((detail_x, card_y + 104), "Suhu Awal: 95°C ±1°C | Suhu Ruang Pengujian: 20°C ±2°C", font=font_body_bold, fill=INK)
    draw.text((detail_x, card_y + 138), "Spesifikasi resmi produsen Zojirushi Corporation (Kapasitas 0,48 L / 480 ml).", font=font_body, fill=MUTED)
    draw.text((detail_x, card_y + 168), "STATUS: FAKTA TERVERIFIKASI (ID KLAIM N-01, N-02, N-03)", font=font_label, fill=MUTED)

    # Footer Provenance
    draw.line([(margin_x, 1850), (margin_x + content_w, 1850)], fill=LINE, width=1)
    draw.text((margin_x, 1865), "FRAMEWORK VIDEO PENJELASAN 3D — STYLE BOARD SAMPLE V0.1", font=font_label, fill=MUTED)
    draw.text((margin_x + content_w - 220, 1865), "VOLT DESIGN SYSTEM 1.1", font=font_label, fill=MUTED)

    # Save outputs
    base.save(OUT_PNG)
    base.convert("RGB").save(OUT_JPG, quality=95)
    print(f"Master Style Board Frame saved to:\n- {OUT_PNG}\n- {OUT_JPG}")


if __name__ == "__main__":
    main()
