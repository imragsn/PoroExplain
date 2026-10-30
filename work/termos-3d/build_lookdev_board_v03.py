import os
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
MIRROR_ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style_antigravity"
OUTPUTS = os.path.join(ROOT, "outputs")
MIRROR_OUTPUTS = os.path.join(MIRROR_ROOT, "outputs")

ARIAL_REG = r"C:\Windows\Fonts\arial.ttf"
ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"

HERO_IMG = os.path.join(OUTPUTS, "termos-03-lookdev-hero-v0.3.png")
PEELED_IMG = os.path.join(OUTPUTS, "termos-03-lookdev-peeled-v0.3.png")
ANCHORS_JSON = os.path.join(OUTPUTS, "termos-03-anchors-semi-realis-v0.3.json")
BOARD_OUT = os.path.join(OUTPUTS, "termos-03-lookdev-sheet-v0.3.png")

# Authentic VOLT DS Tokens
INK = "#101110"
PAPER = "#FFFFFA"
ELECTRIC = "#E8F500"
WASH = "#F7FACD"
MUTED = "#595D52"
LINE = "#919587"


def font_reg(size):
    return ImageFont.truetype(ARIAL_REG, size)


def font_bold(size):
    return ImageFont.truetype(ARIAL_BOLD, size)


def draw_tracked_text(draw, xy, text, font, fill=INK, tracking=0.0):
    """
    Draws text with exact CSS-like letter-spacing (tracking in px).
    VOLT DS uses negative tracking (-0.055em to -0.065em) on bold display/headings,
    and positive tracking (+0.08em) on micro eyebrows.
    """
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        w = draw.textlength(ch, font=font)
        x += w + tracking
    return x


def measure_tracked_text(draw, text, font, tracking=0.0):
    if not text:
        return 0
    total = 0.0
    for ch in text:
        total += draw.textlength(ch, font=font) + tracking
    return total - tracking


def draw_multiline_tracked(draw, xy, lines, font, fill=INK, tracking=0.0, line_height_px=40):
    x, y = xy
    for line in lines:
        draw_tracked_text(draw, (x, y), line, font, fill=fill, tracking=tracking)
        y += line_height_px
    return y


def draw_volt_annotation(draw, pin_xy, box_xy, index_str, title_str, desc_str, is_electric=False, align_right=False):
    """
    Authentic VOLT DS C13 Annotation + SH01 Frame:
    - Clean 1.5px-2px solid #101110 border, zero corner radius, ZERO drop-shadow.
    - Micro index eyebrow ('01 / LAPISAN LUAR') in small tracked uppercase.
    - Bold tight-tracked headline ('CANGKANG ICE GRAY.').
    - Sentence-case supporting description ('Pintu belah radial manifold 1.4 mm.').
    """
    px, py = pin_xy
    bx, by = box_xy

    f_micro = font_reg(12)
    f_title = font_bold(22)
    f_desc = font_reg(15)

    w_micro = measure_tracked_text(draw, index_str, f_micro, tracking=1.0)
    w_title = measure_tracked_text(draw, title_str, f_title, tracking=-1.1)
    w_desc = measure_tracked_text(draw, desc_str, f_desc, tracking=0.0)

    w_box = int(max(w_micro, w_title, w_desc) + 40)
    h_box = 92

    if align_right:
        bx = 2340 - w_box

    # Clean orthogonal 2px Ink leader line
    target_x = bx if bx > px else bx + w_box
    target_y = by + 46
    mid_x = int(px + (target_x - px) * 0.52)
    draw.line([(px, py), (mid_x, py), (mid_x, target_y), (target_x, target_y)], fill=INK, width=2)

    # Square angular pin marker (VOLT SH04 / ICON01 square geometry, zero radius)
    r = 5
    pin_fill = ELECTRIC if is_electric else PAPER
    draw.rectangle((px - r, py - r, px + r, py + r), fill=pin_fill, outline=INK, width=2)

    # Box surface (Paper default; Electric only for the primary focal highlight)
    bg_fill = ELECTRIC if is_electric else PAPER
    draw.rectangle((bx, by, bx + w_box, by + h_box), fill=bg_fill, outline=INK, width=2)

    # 1. Micro Eyebrow
    draw_tracked_text(draw, (bx + 18, by + 14), index_str, f_micro, fill=INK if is_electric else MUTED, tracking=1.0)
    # 2. Bold Tight-Tracked Title
    draw_tracked_text(draw, (bx + 18, by + 34), title_str, f_title, fill=INK, tracking=-1.1)
    # 3. Sentence-case description
    draw_tracked_text(draw, (bx + 18, by + 64), desc_str, f_desc, fill=INK if is_electric else MUTED, tracking=0.0)


def main():
    hero = Image.open(HERO_IMG).convert("RGB")
    peeled = Image.open(PEELED_IMG).convert("RGB")
    with open(ANCHORS_JSON, "r", encoding="utf-8") as f:
        anchors = json.load(f)["lookdev_peeled"]

    # Create a 2400 x 1920 VOLT Modular Architectural Sheet:
    # Left Column (480px): VOLT Editorial Spec & Metric Grid (like Screenshot 3: '02 / EXPLAIN - ONE VIEW. THREE SIGNALS.')
    # Middle Column (840px): LookDev 01 Hero Exterior (cropped centered around bottle)
    # Right Column (1080px): LookDev 02 Multi-Layer Peel + Clean VOLT Annotations
    W, H = 2400, 1920
    board = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(board)

    # Paste Hero in middle column (X = 480..1320, width = 840)
    hero_crop = hero.crop((120, 0, 960, 1920))
    board.paste(hero_crop, (480, 0))

    # Paste Peeled in right column (X = 1320..2400, width = 1080)
    board.paste(peeled, (1320, 0))

    # --------------------------------------------------------------------------
    # LEFT COLUMN (X = 0..480): AUTHENTIC VOLT DS EDITORIAL & METRIC GRID
    # --------------------------------------------------------------------------
    # Top Electric Hero Block (X = 0..480, Y = 0..660)
    draw.rectangle((0, 0, 480, 660), fill=ELECTRIC, outline=INK, width=2)

    f_micro = font_reg(13)
    f_display = font_bold(64)
    f_body = font_reg(19)
    f_metric_big = font_bold(96)
    f_metric_med = font_bold(54)
    f_label = font_reg(16)

    draw_tracked_text(draw, (44, 48), "03 / LOOKDEV GATE / SEMI-REALIS", f_micro, fill=INK, tracking=1.1)

    draw_multiline_tracked(
        draw,
        (44, 110),
        ["SATU MODEL.", "LIMA LAPIS.", "PRESISI 1:1."],
        f_display,
        fill=INK,
        tracking=-3.6,
        line_height_px=60,
    )

    body_lines = [
        "Geometri solid manifold Zojirushi",
        "SM-WA48 dengan pencahayaan",
        "fisik Cycles dan tipografi modular",
        "VOLT Design System.",
    ]
    y_cur = 330
    for bl in body_lines:
        draw_tracked_text(draw, (44, y_cur), bl, f_body, fill=INK, tracking=-0.2)
        y_cur += 28

    # Mini pill tags at bottom of Electric Hero block (like Screenshot 1)
    tags = ["Solid Manifold", "SSS Silicone", "Cycles AgX"]
    tx = 44
    for tg in tags:
        tw = int(measure_tracked_text(draw, tg, font_reg(13), 0.0) + 28)
        draw.rectangle((tx, 576, tx + tw, 616), fill=ELECTRIC, outline=INK, width=1)
        draw.text((tx + 14, 588), tg, font=font_reg(13), fill=INK)
        tx += tw + 10

    # Middle 2-Column Metric Grid (X = 0..480, Y = 660..960) — Like '128 / 4' in Screenshot 3
    draw.rectangle((0, 660, 240, 960), fill=PAPER, outline=INK, width=1)
    draw.rectangle((240, 660, 480, 960), fill=PAPER, outline=INK, width=1)

    draw_tracked_text(draw, (44, 700), "21,5", f_metric_med, fill=INK, tracking=-2.5)
    draw_tracked_text(draw, (152, 718), "cm", font_bold(28), fill=INK, tracking=-1.0)
    draw_tracked_text(draw, (44, 780), "Tinggi total 1:1", f_label, fill=INK)
    draw_tracked_text(draw, (44, 806), "Diameter bodi 6,5 cm", font_reg(14), fill=MUTED)

    draw_tracked_text(draw, (280, 700), "5", f_metric_med, fill=INK, tracking=-2.5)
    draw_tracked_text(draw, (280, 780), "Lapisan kupasan", f_label, fill=INK)
    draw_tracked_text(draw, (280, 806), "Concentric + Axial Explode", font_reg(14), fill=MUTED)

    # Big Highlight Metric Cell (X = 0..480, Y = 960..1420) — Like '85.6%' in Screenshot 3
    draw.rectangle((0, 960, 480, 1420), fill=WASH, outline=INK, width=1)
    draw_tracked_text(draw, (44, 996), "BUKTI RETENSI TERMAL (JIS S 2006)", f_micro, fill=MUTED, tracking=1.0)
    draw_tracked_text(draw, (44, 1045), "≥71", f_metric_big, fill=INK, tracking=-4.5)
    draw_tracked_text(draw, (212, 1068), "°C", font_bold(56), fill=INK, tracking=-2.0)
    draw_tracked_text(draw, (44, 1180), "Suhu air setelah 6 jam penuh", font_bold(20), fill=INK, tracking=-0.5)
    draw_tracked_text(draw, (44, 1214), "Kondisi awal 95°C ± 1°C pada suhu ruang 20°C ± 2°C.", font_reg(15), fill=MUTED)
    draw_tracked_text(draw, (44, 1240), "Celah vakum ~1 mm diperbesar skematis 2 mm.", font_reg(15), fill=MUTED)

    # Bottom Spec Table / Provenance Cell (X = 0..480, Y = 1420..1920)
    draw.rectangle((0, 1420, 480, 1920), fill=INK, outline=INK, width=2)
    draw_tracked_text(draw, (44, 1464), "04 / PARAMETER MATERIAL 3D", f_micro, fill=ELECTRIC, tracking=1.0)
    draw_multiline_tracked(
        draw,
        (44, 1506),
        ["SHADING FISIK.", "TANPA GARIS", "KARTUN."],
        font_bold(40),
        fill=PAPER,
        tracking=-1.8,
        line_height_px=42,
    )
    specs = [
        "• Cangkang: Matte Ice Gray (#73868A), Coat 0.32",
        "• Stopper: Silicone SSS (Subsurface Weight 0.82)",
        "• Perisai: Copper/Gold Mirror (Metallic 0.96)",
        "• Tabung: Brushed Stainless SUS304 (Aniso 0.42)",
        "• Kamera: Lensa 68mm DoF f/4.5, AgX Contrast",
    ]
    sy = 1665
    for sp in specs:
        draw_tracked_text(draw, (44, sy), sp, font_reg(15), fill=PAPER, tracking=0.0)
        sy += 34

    # --------------------------------------------------------------------------
    # TOP HEADERS FOR MIDDLE & RIGHT 3D VIEWPORT PANELS (Clean 2px Frame Bars)
    # --------------------------------------------------------------------------
    # Structural vertical dividers
    draw.line([(480, 0), (480, 1920)], fill=INK, width=2)
    draw.line([(1320, 0), (1320, 1920)], fill=INK, width=2)
    draw.rectangle((0, 0, W - 1, H - 1), outline=INK, width=2)

    # Middle Header Bar (X = 480..1320, Y = 0..116)
    draw.rectangle((480, 0, 1320, 116), fill=PAPER, outline=INK, width=2)
    draw_tracked_text(draw, (516, 24), "01 / EXTERIOR UTUH (HERO SHOT)", f_micro, fill=MUTED, tracking=1.0)
    draw_tracked_text(draw, (516, 52), "SILUET 1:1 MATTE ICE GRAY.", font_bold(32), fill=INK, tracking=-1.6)

    # Right Header Bar (X = 1320..2400, Y = 0..116)
    draw.rectangle((1320, 0, 2400, 116), fill=PAPER, outline=INK, width=2)
    draw_tracked_text(draw, (1356, 24), "02 / MULTI-LAYER CONCENTRIC PEEL + AXIAL EXPLODED", f_micro, fill=MUTED, tracking=1.0)
    draw_tracked_text(draw, (1356, 52), "BEDAH LIMA LAPISAN PENAHAN PANAS.", font_bold(32), fill=INK, tracking=-1.6)

    # --------------------------------------------------------------------------
    # CLEAN VOLT ANNOTATIONS ON RIGHT PANEL (Offset X by +1320)
    # --------------------------------------------------------------------------
    def p_xy(key):
        a = anchors[key]
        return (1320 + a["x_px"], a["y_px"])

    draw_volt_annotation(
        draw,
        p_xy("ANCHOR_CAP_LID"),
        (1960, 250),
        "AXIAL 01 / MEKANISME TUTUP",
        "TUTUP FLIP & PENGUNCI.",
        "Engsel belakang dengan bevel halus 0,8 mm.",
        is_electric=False,
        align_right=True,
    )
    draw_volt_annotation(
        draw,
        p_xy("ANCHOR_SILICONE_STOPPER"),
        (1960, 455),
        "AXIAL 02 / PENAHAN KONVEKSI",
        "STOPPER SILIKON SSS.",
        "Subsurface scattering kenyal pengunci uap.",
        is_electric=False,
        align_right=True,
    )
    draw_volt_annotation(
        draw,
        p_xy("ANCHOR_MOUTHPIECE_SPOUT"),
        (1356, 535),
        "AXIAL 03 / LEHER BOTOL",
        "CORONG MINUM 4,0 CM.",
        "Polypropylene hangat + cincin gasket rapat.",
        is_electric=False,
        align_right=False,
    )
    draw_volt_annotation(
        draw,
        p_xy("ANCHOR_OUTER_SHELL_ICEGRAY"),
        (1356, 860),
        "LAPISAN 01 / PELINDUNG LUAR",
        "CANGKANG ICE GRAY.",
        "Pintu belah radial manifold tertutup.",
        is_electric=False,
        align_right=False,
    )
    # Primary Focal Highlight uses VOLT Electric Yellow (#E8F500) — One main signal highlight!
    draw_volt_annotation(
        draw,
        p_xy("ANCHOR_VACUUM_GAP_2MM"),
        (1960, 755),
        "LAPISAN 02 / KUNCI UTAMA ISOLASI",
        "CELAH VAKUM ~2 MM.",
        "Ruang hampa udara pemutus rambat panas.",
        is_electric=True,
        align_right=True,
    )
    draw_volt_annotation(
        draw,
        p_xy("ANCHOR_COPPER_GOLD_MIRROR"),
        (1960, 1005),
        "LAPISAN 03 / PENANGKAL RADIASI",
        "CERMIN TEMBAGA EMAS.",
        "Foil reflektif pemantul gelombang panas.",
        is_electric=False,
        align_right=True,
    )
    draw_volt_annotation(
        draw,
        p_xy("ANCHOR_INNER_STEEL_SUS304"),
        (1960, 1255),
        "LAPISAN 04 / DINDING DALAM",
        "TABUNG BAJA SUS304.",
        "Permukaan baja tahan karat higienis.",
        is_electric=False,
        align_right=True,
    )
    draw_volt_annotation(
        draw,
        p_xy("ANCHOR_HOT_LIQUID_CORE"),
        (1356, 1265),
        "LAPISAN 05 / INTI ENERGI",
        "KOLOM AIR PANAS 480 ML.",
        "Inti cairan 95°C dengan panah pantul 3D.",
        is_electric=False,
        align_right=False,
    )

    # Bottom Footer Bar across Middle & Right panels (Y = 1856..1920)
    draw.rectangle((480, 1856, 2400, 1920), fill=PAPER, outline=INK, width=2)
    draw_tracked_text(
        draw,
        (516, 1880),
        "VOLT DESIGN SYSTEM 1.1  ·  3D SEMI-REALISTIC LOOKDEV GATE  ·  SUMBER DATA: ZOJIRUSHI SM-WA48 (JIS S 2006)",
        f_micro,
        fill=MUTED,
        tracking=0.8,
    )

    board.save(BOARD_OUT, "PNG")
    shutil.copy2(BOARD_OUT, os.path.join(MIRROR_OUTPUTS, os.path.basename(BOARD_OUT)))
    print(f"Saved Authentic VOLT LookDev Sheet: {BOARD_OUT}")


if __name__ == "__main__":
    main()
