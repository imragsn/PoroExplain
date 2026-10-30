"""
Master Video Animation Assembly v0.4 (Full Universal SOP Implementation)
========================================================================
- True 3D sequential frames rendered from Blender 5.2 EEVEE Next (v0.4 rig)
- 8-Part Cinematic Camera Choreography & Speed Ramping
- Adaptive Kinetic Typography Badges ([ KLIK! ], [ HAMPA VAKUM ], [ 98% REFLEKSI ])
- Conditional VOLT DS Pin Labels with Animated Leader-Line Draw & Spring Pop
- Data-Driven 3-Beat Metric Punch (Scale Pop 1.35x on ≥71°C)
- Zero-Latency Karaoke Subtitles with Active Word Chip
- Master Audio with Procedural Sound Design Foley (Clicks, Whooshes, Pings, Sub-Drop)
"""

import os
import sys
import re
import math
import time
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
OUTPUTS_DIR = os.path.join(ROOT, "outputs")
FRAMES_DIR = os.path.join(ROOT, "work", "termos-3d", "anim_frames_v04")
ANCHORS_FILE = os.path.join(OUTPUTS_DIR, "termos-05-anim-anchors-v0.4.json")
AUDIO_FILE = os.path.join(OUTPUTS_DIR, "termos-04-master-audio-v0.4.mp3")
SRT_FILE = os.path.join(OUTPUTS_DIR, "termos-04-cue-kata-v0.2.srt")

OUT_MP4 = os.path.join(OUTPUTS_DIR, "termos-06-animasi-master-semi-realis-v0.4.mp4")

# VOLT DS 1.1 Color Tokens
INK = (16, 17, 16, 255)            # #101110
PAPER = (255, 255, 250, 255)       # #FFFFFA
ELECTRIC = (232, 245, 0, 255)      # #E8F500
MUTED = (89, 93, 82, 255)          # #595D52
BORDER = (16, 17, 16, 255)         # 1.5px - 2px Solid Ink
LINE_LIGHT = (210, 214, 204, 255)
POSITIVE = (35, 94, 66, 255)       # #235E42

FPS = 30
TOTAL_DURATION = 55.968
TOTAL_FRAMES = 1680

# Windows Typography: Arial Bold & Regular for Authentic VOLT DS
FONT_ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_ARIAL_REG = r"C:\Windows\Fonts\arial.ttf"

font_header_title = ImageFont.truetype(FONT_ARIAL_BOLD, 52)
font_header_eyebrow = ImageFont.truetype(FONT_ARIAL_REG, 17)
font_meta_stamp = ImageFont.truetype(FONT_ARIAL_REG, 13)

font_pin_tag = ImageFont.truetype(FONT_ARIAL_BOLD, 14)
font_pin_title = ImageFont.truetype(FONT_ARIAL_BOLD, 22)
font_pin_desc = ImageFont.truetype(FONT_ARIAL_REG, 15)

font_badge_bold = ImageFont.truetype(FONT_ARIAL_BOLD, 24)
font_badge_sfx = ImageFont.truetype(FONT_ARIAL_BOLD, 28)

font_metric_eyebrow = ImageFont.truetype(FONT_ARIAL_REG, 14)
font_metric_mid = ImageFont.truetype(FONT_ARIAL_BOLD, 46)
font_metric_big = ImageFont.truetype(FONT_ARIAL_BOLD, 74)
font_metric_note = ImageFont.truetype(FONT_ARIAL_BOLD, 18)

font_sub_active = ImageFont.truetype(FONT_ARIAL_BOLD, 36)
font_sub_normal = ImageFont.truetype(FONT_ARIAL_REG, 34)


def spring_val(t, damping=14.0, stiffness=120.0, mass=0.8):
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    omega = math.sqrt(stiffness / mass)
    zeta = damping / (2.0 * math.sqrt(stiffness * mass))
    decay = math.exp(-zeta * omega * t)
    return 1.0 - decay * math.cos(omega * t)


def ease_out_cubic(t):
    return 1.0 - (1.0 - t) ** 3


def draw_text_tracked(draw, xy, text, font, fill=INK, tracking_em=-0.05):
    x, y = xy
    font_size = getattr(font, "size", 30)
    spacing = int(font_size * tracking_em)
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bbox = font.getbbox(ch)
        cw = bbox[2] - bbox[0] if bbox else 10
        x += cw + spacing
    return x


def measure_text_tracked(font, text, tracking_em=-0.05):
    font_size = getattr(font, "size", 30)
    spacing = int(font_size * tracking_em)
    tot_w = 0
    max_h = 0
    for ch in text:
        bbox = font.getbbox(ch)
        if bbox:
            cw = bbox[2] - bbox[0]
            ch_h = bbox[3] - bbox[1]
            tot_w += cw + spacing
            if ch_h > max_h:
                max_h = ch_h
        else:
            tot_w += spacing
    return max(0, tot_w - spacing), max_h


def parse_srt(srt_path):
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = []
    pattern = re.compile(
        r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)",
        re.DOTALL
    )
    for m in pattern.finditer(content):
        idx = int(m.group(1))
        def to_sec(ts):
            h, m_val, s_ms = ts.split(":")
            s, ms = s_ms.split(",")
            return int(h) * 3600 + int(m_val) * 60 + int(s) + int(ms) / 1000.0
        start = to_sec(m.group(2))
        end = to_sec(m.group(3))
        word = m.group(4).strip()
        entries.append({"id": idx, "start": start, "end": end, "word": word})
    return entries


def build_subtitle_chunks(words):
    chunks = []
    cur = []
    for w in words:
        cur.append(w)
        if len(cur) == 4 or (len(cur) >= 2 and w["word"].endswith((".", "?", "!", "..."))):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def get_subtitle_at_frame(chunks, frame_idx):
    t = frame_idx / float(FPS)
    for i, c in enumerate(chunks):
        t0 = c[0]["start"]
        t1 = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else c[-1]["end"] + 0.4
        if t0 <= t < t1:
            active_w = next((w for w in c if w["start"] <= t < w["end"]), None)
            return c, active_w
    return None, None


HEADER_PHASES = [
    {
        "start_frame": 0,
        "end_frame": 159,
        "eyebrow": "DARI KESEHARIAN KITA / ZOJIRUSHI SM-WA48",
        "title_lines": ["PAGI DISEDUH.", "SIANG MASIH PANAS."]
    },
    {
        "start_frame": 160,
        "end_frame": 456,
        "eyebrow": "KITA BELAH DUA / DUA DINDING BAJA",
        "title_lines": ["KOSONG DI TENGAH,", "PANAS NGGAK LEWAT."]
    },
    {
        "start_frame": 457,
        "end_frame": 612,
        "eyebrow": "NGGAK ADA UDARA / HAMPA VAKUM",
        "title_lines": ["JALANNYA BUNTU."]
    },
    {
        "start_frame": 613,
        "end_frame": 915,
        "eyebrow": "JALUR TERSEMBUNYI / RADIASI INFRAMERAH",
        "title_lines": ["GELOMBANGNYA", "DIPANTULIN BALIK."]
    },
    {
        "start_frame": 916,
        "end_frame": 1167,
        "eyebrow": "MULUT BOTOL / TUTUP SILIKON SSS",
        "title_lines": ["DIKUNCI RAPAT,", "BOCOR DIKIT DI LEHER."]
    },
    {
        "start_frame": 1168,
        "end_frame": 1593,
        "eyebrow": "ANGKA NYATANYA / UJI RESMI JIS S 2006",
        "title_lines": ["ENAM JAM,", "TETAP DI ATAS 71°C."]
    },
    {
        "start_frame": 1594,
        "end_frame": 1679,
        "eyebrow": "RAHASIA TERMOS / SIAP SETIAP SAAT",
        "title_lines": ["TIAP KALI DITUANG."]
    }
]


def get_header_for_frame(frame_idx):
    for h in HEADER_PHASES:
        if h["start_frame"] <= frame_idx <= h["end_frame"]:
            return h
    return HEADER_PHASES[-1]


def interpolate_anchor(anchors_data, frame_idx, anchor_name):
    keys = sorted([int(k) for k in anchors_data.keys()])
    if not keys:
        return 540, 960, False

    if frame_idx <= keys[0]:
        d = anchors_data[str(keys[0])].get(anchor_name, {})
        return d.get("x_px", 540), d.get("y_px", 960), d.get("visible", False)
    if frame_idx >= keys[-1]:
        d = anchors_data[str(keys[-1])].get(anchor_name, {})
        return d.get("x_px", 540), d.get("y_px", 960), d.get("visible", False)

    k_lower = keys[0]
    k_upper = keys[-1]
    for k in keys:
        if k <= frame_idx:
            k_lower = k
        if k >= frame_idx:
            k_upper = k
            break

    d0 = anchors_data[str(k_lower)].get(anchor_name, {})
    d1 = anchors_data[str(k_upper)].get(anchor_name, {})
    vis = d0.get("visible", False) or d1.get("visible", False)

    if k_lower == k_upper:
        return d0.get("x_px", 540), d0.get("y_px", 960), vis

    t = (frame_idx - k_lower) / float(k_upper - k_lower)
    x = int(d0.get("x_px", 540) * (1 - t) + d1.get("x_px", 540) * t)
    y = int(d0.get("y_px", 960) * (1 - t) + d1.get("y_px", 960) * t)
    return x, y, vis


def draw_volt_pin_card_animated(draw, x_anchor, y_anchor, box_x, box_y, box_w, box_h,
                                tag, title, desc, anim_prog=1.0, is_active=True):
    """
    Kinetic VOLT DS Pin Card with Animated Line Draw & Spring Pop:
    - Phase 1 (prog 0.0 - 0.4): Leader line draws out from anchor
    - Phase 2 (prog 0.4 - 1.0): Card pops in with spring overshoot scale
    """
    if anim_prog <= 0.02:
        return

    # 1. Anchor square point
    dot_color = ELECTRIC if is_active else PAPER
    draw.rectangle([x_anchor - 5, y_anchor - 5, x_anchor + 5, y_anchor + 5], fill=dot_color, outline=INK, width=2)

    # Calculate target connection point on card
    if x_anchor > (box_x + box_w):
        target_x = box_x + box_w
        target_y = box_y + box_h // 2
        elbow_x = target_x + (x_anchor - target_x) // 2
        p1 = (x_anchor, y_anchor)
        p2 = (elbow_x, y_anchor)
        p3 = (elbow_x, target_y)
        p4 = (target_x, target_y)
    elif x_anchor < box_x:
        target_x = box_x
        target_y = box_y + box_h // 2
        elbow_x = x_anchor + (target_x - x_anchor) // 2
        p1 = (x_anchor, y_anchor)
        p2 = (elbow_x, y_anchor)
        p3 = (elbow_x, target_y)
        p4 = (target_x, target_y)
    else:
        target_x = box_x + box_w // 2
        target_y = box_y if y_anchor < box_y else box_y + box_h
        p1 = (x_anchor, y_anchor)
        p2 = (x_anchor, (y_anchor + target_y) // 2)
        p3 = (target_x, (y_anchor + target_y) // 2)
        p4 = (target_x, target_y)

    # 2. Animated Line Draw
    line_prog = min(1.0, anim_prog / 0.5)
    if line_prog < 0.5:
        sub_p = line_prog / 0.5
        curr_p2 = (int(p1[0] + (p2[0] - p1[0]) * sub_p), int(p1[1] + (p2[1] - p1[1]) * sub_p))
        draw.line([p1, curr_p2], fill=INK, width=2)
    elif line_prog < 0.8:
        draw.line([p1, p2], fill=INK, width=2)
        sub_p = (line_prog - 0.5) / 0.3
        curr_p3 = (int(p2[0] + (p3[0] - p2[0]) * sub_p), int(p2[1] + (p3[1] - p2[1]) * sub_p))
        draw.line([p2, curr_p3], fill=INK, width=2)
    else:
        draw.line([p1, p2], fill=INK, width=2)
        draw.line([p2, p3], fill=INK, width=2)
        sub_p = (line_prog - 0.8) / 0.2
        curr_p4 = (int(p3[0] + (p4[0] - p3[0]) * sub_p), int(p3[1] + (p4[1] - p3[1]) * sub_p))
        draw.line([p3, curr_p4], fill=INK, width=2)

    # 3. Card Box Spring Pop-in
    if anim_prog > 0.4:
        box_sub_prog = (anim_prog - 0.4) / 0.6
        scale = 0.82 + 0.18 * spring_val(box_sub_prog, damping=14.0, stiffness=120.0)
        cur_w = int(box_w * scale)
        cur_h = int(box_h * scale)
        cx = box_x + (box_w - cur_w) // 2
        cy = box_y + (box_h - cur_h) // 2

        draw.rectangle([cx, cy, cx + cur_w, cy + cur_h], fill=PAPER, outline=INK, width=2)

        header_h = 28
        header_bg = ELECTRIC if is_active else PAPER
        draw.rectangle([cx, cy, cx + cur_w, cy + header_h], fill=header_bg, outline=INK, width=2)
        draw_text_tracked(draw, (cx + 14, cy + 6), tag.upper(), font_pin_tag, fill=INK, tracking_em=+0.06)

        pad_x = 16
        draw_text_tracked(draw, (cx + pad_x, cy + 36), title.upper(), font_pin_title, fill=INK, tracking_em=-0.04)
        draw_text_tracked(draw, (cx + pad_x, cy + 66), desc, font_pin_desc, fill=MUTED, tracking_em=0.0)


def draw_kinetic_badge(draw, text, cx, cy, prog, bg_color=ELECTRIC, text_color=INK, is_implode=False):
    """
    Adaptive Kinetic Onomatopoeia & Semantic Badges:
    - Pop-in elastic spring scale
    - Crisp 2px black border, sharp zero radius
    """
    if prog <= 0.0 or prog >= 1.0:
        return

    if is_implode:
        # Implosion effect: starts big, contracts rapidly to tight lock
        scale = 1.35 - 0.35 * ease_out_cubic(prog)
    else:
        # Elastic spring pop: bursts in, overshoots, settles
        scale = 0.6 + 0.4 * spring_val(prog * 1.5 if prog < 0.66 else 1.0, damping=12.0, stiffness=140.0)

    tw, th = measure_text_tracked(font_badge_sfx, text, tracking_em=-0.03)
    bw = int((tw + 36) * scale)
    bh = int((th + 20) * scale)
    bx = cx - bw // 2
    by = cy - bh // 2

    draw.rectangle([bx, by, bx + bw, by + bh], fill=bg_color, outline=INK, width=2)
    # Centered text
    tx = bx + (bw - int(tw * scale)) // 2
    ty = by + (bh - int(th * scale)) // 2 - 2
    draw_text_tracked(draw, (tx, ty), text, font_badge_sfx, fill=text_color, tracking_em=-0.03)


def draw_metric_card_3beat(draw, x, y, w, h, anim_prog, punch_prog=0.0):
    """
    Data-Driven 3-Beat Metric Punch:
    - Beat 1 (Entrance): Spring slide in
    - Beat 2 (Scale Punch): Digit ≥71°C springs up to 1.35x when VO triggers
    - Beat 3 (Signal Pulse): Yellow flash border
    """
    if anim_prog <= 0.05:
        return

    # Base container
    draw.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=2)

    # Horizontal split
    split_y = y + 110
    draw.line([(x, split_y), (x + w, split_y)], fill=INK, width=2)

    # Vertical split top row
    split_x = x + w // 2
    draw.line([(split_x, y), (split_x, split_y)], fill=INK, width=2)

    # Top Left Cell: Suhu Awal
    draw_text_tracked(draw, (x + 24, y + 18), "SUHU AWAL (0 JAM)", font_metric_eyebrow, fill=MUTED, tracking_em=+0.06)
    draw_text_tracked(draw, (x + 24, y + 42), "95°C", font_metric_mid, fill=INK, tracking_em=-0.05)

    # Top Right Cell: Durasi Uji
    draw_text_tracked(draw, (split_x + 24, y + 18), "DURASI UJI / 20°C", font_metric_eyebrow, fill=MUTED, tracking_em=+0.06)
    draw_text_tracked(draw, (split_x + 24, y + 42), "6 JAM", font_metric_mid, fill=INK, tracking_em=-0.05)

    # Bottom Cell: Result Banner (Electric Yellow #E8F500)
    draw.rectangle([x, split_y, x + w, y + h], fill=ELECTRIC, outline=INK, width=2)

    # Beat 2 Punch: Big number ≥ 71°C scale pop!
    scale_punch = 1.0
    if punch_prog > 0.0:
        scale_punch = 1.0 + 0.35 * math.sin(punch_prog * math.pi)

    draw_text_tracked(draw, (x + 28, split_y + 16), "STANDAR RESMI JIS S 2006", font_pin_tag, fill=INK, tracking_em=+0.08)

    if math.isclose(scale_punch, 1.0, abs_tol=0.02):
        draw_text_tracked(draw, (x + 28, split_y + 44), "≥ 71°C", font_metric_big, fill=INK, tracking_em=-0.06)
    else:
        font_punch = ImageFont.truetype(FONT_ARIAL_BOLD, int(74 * scale_punch))
        draw_text_tracked(draw, (x + 28, split_y + 40 - int(10 * (scale_punch - 1.0))), "≥ 71°C", font_punch, fill=INK, tracking_em=-0.06)

    # Explanatory note on right
    note_x = x + 350
    draw_text_tracked(draw, (note_x, split_y + 36), "TERBUKTI BERTAHAN PANAS", font_metric_note, fill=INK, tracking_em=-0.03)
    draw_text_tracked(draw, (note_x, split_y + 66), "Setelah 6 jam, air tetap di atas 71°C.", font_pin_desc, fill=INK, tracking_em=0.0)
    draw_text_tracked(draw, (note_x, split_y + 92), "Panas terperangkap sempurna di ruang hampa.", font_pin_desc, fill=MUTED, tracking_em=0.0)


def draw_karaoke_subtitles(draw, chunk, active_word, y_pos=1670):
    if not chunk:
        return

    word_items = []
    tot_width = 0
    pad_h = 14
    pad_v = 8

    for w in chunk:
        is_act = (active_word and w["id"] == active_word["id"])
        font = font_sub_active if is_act else font_sub_normal
        w_text = w["word"]
        tw, th = measure_text_tracked(font, w_text, tracking_em=-0.04 if is_act else 0.0)
        chip_w = tw + pad_h * 2
        chip_h = th + pad_v * 2
        word_items.append({
            "word": w_text,
            "is_act": is_act,
            "font": font,
            "text_w": tw,
            "text_h": th,
            "chip_w": chip_w,
            "chip_h": chip_h
        })
        tot_width += chip_w + 12

    tot_width -= 12
    cur_x = (1080 - tot_width) // 2

    for item in word_items:
        cx = cur_x
        cw = item["chip_w"]
        ch = 56
        cy = y_pos

        if item["is_act"]:
            draw.rectangle([cx, cy, cx + cw, cy + ch], fill=ELECTRIC, outline=INK, width=2)
            tx = cx + pad_h
            ty = cy + (ch - item["text_h"]) // 2 - 4
            draw_text_tracked(draw, (tx, ty), item["word"], item["font"], fill=INK, tracking_em=-0.04)
        else:
            draw.rectangle([cx, cy, cx + cw, cy + ch], fill=PAPER, outline=BORDER, width=1)
            tx = cx + pad_h
            ty = cy + (ch - item["text_h"]) // 2 - 4
            draw_text_tracked(draw, (tx, ty), item["word"], item["font"], fill=INK, tracking_em=0.0)

        cur_x += cw + 12


def render_frame_overlay_v04(frame_img, frame_idx, anchors_data, sub_chunks):
    draw = ImageDraw.Draw(frame_img)
    margin_x = 64

    # --------------------------------------------------------------------------
    # 1. VOLT DS Dynamic Header (7 Locked Conversational Phases)
    # --------------------------------------------------------------------------
    header = get_header_for_frame(frame_idx)
    head_y = 68

    draw_text_tracked(draw, (margin_x, head_y), header["eyebrow"].upper(), font_header_eyebrow, fill=MUTED, tracking_em=+0.08)

    ty = head_y + 32
    for t_line in header["title_lines"]:
        draw_text_tracked(draw, (margin_x, ty), t_line.upper(), font_header_title, fill=INK, tracking_em=-0.06)
        ty += 54

    rule_y = 232
    draw.line([(margin_x, rule_y), (1080 - margin_x, rule_y)], fill=INK, width=2)
    draw.rectangle([margin_x - 4, rule_y - 4, margin_x + 4, rule_y + 4], fill=ELECTRIC, outline=INK, width=1)
    draw_text_tracked(draw, (1080 - margin_x - 170, head_y + 2), "VOLT // SEC.04", font_meta_stamp, fill=MUTED, tracking_em=+0.08)

    # --------------------------------------------------------------------------
    # 2. ADAPTIVE KINETIC ONOMATOPOEIA BADGES
    # --------------------------------------------------------------------------
    # Badge 1: [ KLIK! ] when lid pops open (Frames 118 to 155)
    if 118 <= frame_idx < 155:
        p = (frame_idx - 118) / 37.0
        draw_kinetic_badge(draw, "[ KLIK! ]", cx=620, cy=420, prog=p, bg_color=ELECTRIC, text_color=INK)

    # Badge 2: [ HAMPA VAKUM // 0 MOLEKUL ] when vacuum gap settles (Frames 205 to 290)
    elif 205 <= frame_idx < 290:
        p = (frame_idx - 205) / 85.0
        draw_kinetic_badge(draw, "[ HAMPA VAKUM // 0 MOLEKUL ]", cx=540, cy=580, prog=p, bg_color=INK, text_color=PAPER, is_implode=True)

    # Badge 3: [ 98% REFLEKSI ] when thermal radiation hits gold wall (Frames 680 to 760)
    elif 680 <= frame_idx < 760:
        p = (frame_idx - 680) / 80.0
        draw_kinetic_badge(draw, "[ 98% REFLEKSI ]", cx=420, cy=740, prog=p, bg_color=ELECTRIC, text_color=INK)

    # Badge 4: [ KLIK! ] Outro snap shut (Frames 1635 to 1665)
    elif 1635 <= frame_idx < 1665:
        p = (frame_idx - 1635) / 30.0
        draw_kinetic_badge(draw, "[ KLIK! ]", cx=540, cy=460, prog=p, bg_color=ELECTRIC, text_color=INK)

    # --------------------------------------------------------------------------
    # 3. CONDITIONAL VOLT DS PIN LABELS (Animated Line-Draw & Spring Pop)
    # --------------------------------------------------------------------------
    if frame_idx < 160:
        # Phase 1: Exterior Hero View
        x_out, y_out, vis = interpolate_anchor(anchors_data, frame_idx, "ANCHOR_OUTER_SHELL_ICEGRAY")
        if vis and frame_idx >= 20:
            prog = min(1.0, (frame_idx - 20) / 18.0)
            draw_volt_pin_card_animated(
                draw, x_out, y_out,
                box_x=68, box_y=680, box_w=340, box_h=100,
                tag="01 / EKSTERIOR",
                title="CANGKANG LUAR",
                desc="Matte Ice Gray, SUS304.",
                anim_prog=prog,
                is_active=True
            )

    elif 160 <= frame_idx < 457:
        # Phase 2: Cutaway Peeling (Vacuum Gap & Inner Steel)
        x_vac, y_vac, vis_v = interpolate_anchor(anchors_data, frame_idx, "ANCHOR_VACUUM_GAP_2MM")
        x_in, y_in, vis_i = interpolate_anchor(anchors_data, frame_idx, "ANCHOR_INNER_STEEL_SUS304")
        if vis_v and frame_idx >= 180:
            prog = min(1.0, (frame_idx - 180) / 18.0)
            draw_volt_pin_card_animated(
                draw, x_vac, y_vac,
                box_x=670, box_y=780, box_w=346, box_h=100,
                tag="02 / HAMPA UDARA",
                title="CELAH VAKUM 2 MM",
                desc="Konduksi & konveksi nol.",
                anim_prog=prog,
                is_active=True
            )
        if vis_i and frame_idx >= 210:
            prog = min(1.0, (frame_idx - 210) / 18.0)
            draw_volt_pin_card_animated(
                draw, x_in, y_in,
                box_x=68, box_y=1120, box_w=340, box_h=100,
                tag="03 / DINDING DALAM",
                title="TABUNG SUS304",
                desc="Baja tahan karat murni.",
                anim_prog=prog,
                is_active=False
            )

    elif 613 <= frame_idx < 916:
        # Phase 4: Copper/Gold Mirror & Radiation Bounce
        x_cop, y_cop, vis_c = interpolate_anchor(anchors_data, frame_idx, "ANCHOR_COPPER_GOLD_MIRROR")
        x_liq, y_liq, vis_l = interpolate_anchor(anchors_data, frame_idx, "ANCHOR_HOT_LIQUID_CORE")
        if vis_c and frame_idx >= 630:
            prog = min(1.0, (frame_idx - 630) / 18.0)
            draw_volt_pin_card_animated(
                draw, x_cop, y_cop,
                box_x=660, box_y=960, box_w=356, box_h=100,
                tag="04 / REFLEKTOR",
                title="SELUBUNG EMAS / Cu",
                desc="Pantulkan 98% radiasi.",
                anim_prog=prog,
                is_active=True
            )
        if vis_l and frame_idx >= 650:
            prog = min(1.0, (frame_idx - 650) / 18.0)
            draw_volt_pin_card_animated(
                draw, x_liq, y_liq,
                box_x=68, box_y=1220, box_w=340, box_h=100,
                tag="05 / INTI TERMAL",
                title="AIR PANAS 95°C",
                desc="Panas terperangkap rapi.",
                anim_prog=prog,
                is_active=False
            )

    elif 916 <= frame_idx < 1168:
        # Phase 5: Axial Exploded Stopper & Neck
        x_stp, y_stp, vis_s = interpolate_anchor(anchors_data, frame_idx, "ANCHOR_SILICONE_STOPPER")
        x_spt, y_spt, vis_p = interpolate_anchor(anchors_data, frame_idx, "ANCHOR_MOUTHPIECE_SPOUT")
        if vis_s and frame_idx >= 930:
            prog = min(1.0, (frame_idx - 930) / 18.0)
            draw_volt_pin_card_animated(
                draw, x_stp, y_stp,
                box_x=640, box_y=360, box_w=376, box_h=100,
                tag="06 / PENYEKAT",
                title="STOPPER SILIKON SSS",
                desc="Karet kedap food-grade.",
                anim_prog=prog,
                is_active=True
            )
        if vis_p and frame_idx >= 945:
            prog = min(1.0, (frame_idx - 945) / 18.0)
            draw_volt_pin_card_animated(
                draw, x_spt, y_spt,
                box_x=68, box_y=540, box_w=340, box_h=100,
                tag="07 / CORONG",
                title="MULUT BOTOL 4 CM",
                desc="Bocor minimal di leher.",
                anim_prog=prog,
                is_active=False
            )

    # --------------------------------------------------------------------------
    # 4. DATA-DRIVEN 3-BEAT METRIC PUNCH (Frames 1168–1593)
    # --------------------------------------------------------------------------
    if 1168 <= frame_idx < 1594:
        # Entrance slide with spring
        ent_prog = min(1.0, (frame_idx - 1168) / 24.0)
        card_w = 952
        card_h = 240
        card_x = (1080 - card_w) // 2
        target_y = 1320
        curr_y = int(target_y + (1.0 - math.sin(ent_prog * math.pi * 0.5)) * 60)

        # Scale punch on ≥71°C around frame 1290–1330 (when VO says "di atas 71 derajat")
        punch_p = 0.0
        if 1290 <= frame_idx < 1330:
            punch_p = (frame_idx - 1290) / 40.0

        draw_metric_card_3beat(draw, card_x, curr_y, card_w, card_h, anim_prog=ent_prog, punch_prog=punch_p)

    # --------------------------------------------------------------------------
    # 5. ZERO-LATENCY KARAOKE SUBTITLES
    # --------------------------------------------------------------------------
    chunk, active_w = get_subtitle_at_frame(sub_chunks, frame_idx)
    sub_y = 1620 if (1168 <= frame_idx < 1594) else 1680
    draw_karaoke_subtitles(draw, chunk, active_w, y_pos=sub_y)

    # --------------------------------------------------------------------------
    # 6. SWISS FOOTER STAMP
    # --------------------------------------------------------------------------
    footer_y = 1860
    draw.line([(margin_x, footer_y), (1080 - margin_x, footer_y)], fill=LINE_LIGHT, width=1)
    draw_text_tracked(draw, (margin_x, footer_y + 12), "ZOJIRUSHI SM-WA48 // 480 ML", font_meta_stamp, fill=MUTED, tracking_em=+0.08)
    time_stamp_str = f"{frame_idx / float(FPS):05.2f}S / {TOTAL_DURATION:05.2f}S"
    draw_text_tracked(draw, (1080 - margin_x - 140, footer_y + 12), time_stamp_str, font_meta_stamp, fill=MUTED, tracking_em=+0.06)

    return frame_img


def assemble_video_v04(output_path=OUT_MP4):
    print("=" * 60)
    print("ASSEMBLING MASTER VIDEO v0.4 (Full Universal SOP)")
    print("=" * 60)

    words = parse_srt(SRT_FILE)
    sub_chunks = build_subtitle_chunks(words)
    print(f"Loaded {len(words)} words into {len(sub_chunks)} subtitle chunks.")

    with open(ANCHORS_FILE, "r", encoding="utf-8") as f:
        anchors_data = json.load(f)
    print(f"Loaded tracking anchors: {len(anchors_data)} anchor frames.")

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO_FILE,
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]

    print(f"Launching FFmpeg master encoding pipeline to {output_path}...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    t0 = time.time()
    for f_idx in range(TOTAL_FRAMES):
        frame_file = os.path.join(FRAMES_DIR, f"frame_{f_idx:04d}.png")
        if not os.path.exists(frame_file):
            wait_count = 0
            while not os.path.exists(frame_file) and wait_count < 15:
                time.sleep(1)
                wait_count += 1
            if not os.path.exists(frame_file):
                print(f"Error: Frame {frame_file} missing! Aborting.")
                proc.stdin.close()
                proc.wait()
                return False

        with Image.open(frame_file) as base_img:
            frame_img = base_img.convert("RGBA")
            composed = render_frame_overlay_v04(frame_img, f_idx, anchors_data, sub_chunks)
            proc.stdin.write(composed.tobytes())

        if f_idx % 60 == 0:
            elapsed = time.time() - t0
            fps_proc = (f_idx + 1) / max(0.1, elapsed)
            print(f"Composited frame {f_idx}/{TOTAL_FRAMES - 1} ({fps_proc:.1f} fps)")

    proc.stdin.close()
    proc.wait()
    print(f"Done! Master video v0.4 encoded in {time.time() - t0:.1f}s: {output_path}")
    return True


if __name__ == "__main__":
    assemble_video_v04()
