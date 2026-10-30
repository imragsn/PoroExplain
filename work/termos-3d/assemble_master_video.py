"""
Assemble Master Video Animation (56 Seconds, 1080x1920, 30 fps)
Full Production Build:
- Master Model 3D (Hero 3-Quarter & Frontal Cutaway 5-Layers)
- VOLT Design System + Space Grotesk Typography
- Semantic Color System (Positive Green, Info Blue, Thermal Amber, Wash Tint, Electric Yellow)
- Subtitle Karaoke Engine (max 4 words, center-aligned at X=540, Y=1380, Electric Yellow active highlight)
- Dynamic Kinetic SFX ("KLIK!") and Thermal Radiation Waves
- C02 Metric Evidence Card (slide-up spring entrance at proof cue)
- Seamless Loop Outro
"""
import os
import re
import math
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
OUTPUTS_DIR = os.path.join(ROOT, "outputs")
AUDIO_FILE = os.path.join(OUTPUTS_DIR, "termos-04-narasi-v0.2.mp3")
SRT_FILE = os.path.join(OUTPUTS_DIR, "termos-04-cue-kata-v0.2.srt")
FONT_PATH = os.path.join(ROOT, "work", "fonts", "SpaceGrotesk-VariableFont_wght.ttf")
HERO_BASE = os.path.join(ROOT, "work", "termos-3d", "style_b_hero_transparent.png")
CUTAWAY_BASE = os.path.join(ROOT, "work", "termos-3d", "style_b_base_transparent.png")

OUT_MP4 = os.path.join(OUTPUTS_DIR, "termos-06-animasi-master-v0.1.mp4")

# VOLT DS Color Tokens
INK = (16, 17, 16, 255)            # #101110
PAPER = (255, 255, 250, 255)       # #FFFFFA
ELECTRIC = (232, 245, 0, 255)      # #E8F500
WASH = (247, 250, 205, 255)        # #F7FACD
MUTED = (89, 93, 82, 255)          # #595D52
LINE = (145, 149, 135, 255)        # #919587
POSITIVE = (35, 94, 66, 255)       # #235E42
INFO = (35, 90, 135, 255)          # #235A87
AMBER = (183, 110, 0, 255)         # #B76E00
HEAT_ORANGE = (230, 110, 25, 210)

FPS = 30
TOTAL_DURATION = 55.968
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)  # 1679 frames


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
font_sfx = get_font(24, 700)


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_out_quint(t):
    return 1 - (1 - t) ** 5


def ease_in_out(t):
    return 0.5 * (1 - math.cos(math.pi * t))


def spring_val(t, damping=14, stiffness=110, mass=0.8):
    if t <= 0:
        return 0.0
    if t >= 1.0:
        return 1.0
    omega = math.sqrt(stiffness / mass)
    zeta = damping / (2 * math.sqrt(stiffness * mass))
    decay = math.exp(-zeta * omega * t)
    return 1.0 - decay * math.cos(omega * t)


def parse_srt(srt_path):
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = []
    pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)", re.DOTALL)
    for m in pattern.finditer(content):
        idx = int(m.group(1))
        def to_sec(ts):
            h, m_val, s_ms = ts.split(":")
            s, ms = s_ms.split(",")
            return int(h)*3600 + int(m_val)*60 + int(s) + int(ms)/1000.0
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


def draw_hud_box(draw, x_anchor, y_anchor, x_box, y_box, w_box, h_box, tag, title, body_lines, accent_color, align_right=False, alpha_progress=1.0):
    if alpha_progress <= 0.01:
        return

    scale = 0.85 + 0.15 * ease_out_cubic(alpha_progress)
    cur_w = int(w_box * scale)
    cur_h = int(h_box * scale)
    y_connect = y_box + cur_h // 2

    if align_right:
        x_connect = x_box + cur_w
        elbow_x = (x_connect + x_anchor) // 2
        line_progress = min(1.0, alpha_progress * 1.5)
        # Flowing leader line
        p1 = (x_anchor, y_anchor)
        p2 = (int(x_anchor + (elbow_x - x_anchor) * line_progress), y_anchor)
        draw.line([p1, p2], fill=INK, width=2)
        if line_progress > 0.5:
            lp2 = (line_progress - 0.5) / 0.5
            p3 = (elbow_x, int(y_anchor + (y_connect - y_anchor) * lp2))
            draw.line([p2, p3], fill=INK, width=2)
            p4 = (int(elbow_x + (x_connect - elbow_x) * lp2), y_connect)
            draw.line([p3, p4], fill=INK, width=2)
    else:
        x_connect = x_box
        elbow_x = (x_anchor + x_connect) // 2
        line_progress = min(1.0, alpha_progress * 1.5)
        p1 = (x_anchor, y_anchor)
        p2 = (int(x_anchor + (elbow_x - x_anchor) * line_progress), y_anchor)
        draw.line([p1, p2], fill=INK, width=2)
        if line_progress > 0.5:
            lp2 = (line_progress - 0.5) / 0.5
            p3 = (elbow_x, int(y_anchor + (y_connect - y_anchor) * lp2))
            draw.line([p2, p3], fill=INK, width=2)
            p4 = (int(elbow_x + (x_connect - elbow_x) * lp2), y_connect)
            draw.line([p3, p4], fill=INK, width=2)

    # Pin point
    draw.rectangle([x_anchor - 4, y_anchor - 4, x_anchor + 4, y_anchor + 4], fill=accent_color, outline=INK, width=2)

    # Box content
    if alpha_progress > 0.2:
        draw.rectangle([x_box, y_box, x_box + cur_w, y_box + cur_h], fill=PAPER, outline=INK, width=2)
        header_h = 26
        draw.rectangle([x_box, y_box, x_box + cur_w, y_box + header_h], fill=accent_color)
        draw.text((x_box + 14, y_box + 6), tag.upper(), font=font_tag, fill=PAPER)

        pad_x = 16
        draw.text((x_box + pad_x, y_box + 38), title.upper(), font=font_heading, fill=INK)

        line_y = y_box + 74
        for line in body_lines:
            draw.text((x_box + pad_x, line_y), line, font=font_body, fill=MUTED)
            line_y += 24


def render_video():
    print("Loading master audio & cues...")
    words = parse_srt(SRT_FILE)
    chunks = build_subtitle_chunks(words)
    print(f"Loaded {len(words)} words into {len(chunks)} subtitle chunks.")

    print("Loading 3D transparent layers...")
    img_hero = Image.open(HERO_BASE).convert("RGBA")
    img_cutaway = Image.open(CUTAWAY_BASE).convert("RGBA")

    # Pre-render Tabletop background
    bg_table = Image.new("RGBA", (1080, 1920), PAPER)
    d_tab = ImageDraw.Draw(bg_table)
    for y in range(1220):
        r = int(252 - (y / 1220) * 8)
        g = int(250 - (y / 1220) * 9)
        b = int(246 - (y / 1220) * 12)
        d_tab.line([(0, y), (1080, y)], fill=(r, g, b, 255))
    table_top_y = 1220
    d_tab.rectangle([0, table_top_y, 1080, 1920], fill=(238, 232, 222, 255))
    d_tab.line([(0, table_top_y), (1080, table_top_y)], fill=(215, 208, 196, 255), width=2)
    d_tab.line([(0, table_top_y + 2), (1080, table_top_y + 2)], fill=(248, 245, 240, 255), width=1)

    # Floor shadow
    shadow_table = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_table)
    s_draw.ellipse([340, 1238, 740, 1262], fill=(60, 50, 40, 90))
    s_draw.ellipse([360, 1242, 720, 1258], fill=(40, 30, 20, 140))
    shadow_table = shadow_table.filter(ImageFilter.GaussianBlur(radius=8))
    bg_table.alpha_composite(shadow_table)

    # Pre-render Clean Studio background with floor contact shadow
    bg_clean = Image.new("RGBA", (1080, 1920), PAPER)
    shadow_clean = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    sc_draw = ImageDraw.Draw(shadow_clean)
    sc_draw.ellipse([330, 1238, 750, 1262], fill=(16, 17, 16, 45))
    sc_draw.ellipse([360, 1242, 720, 1258], fill=(16, 17, 16, 75))
    shadow_clean = shadow_clean.filter(ImageFilter.GaussianBlur(radius=7))
    bg_clean.alpha_composite(shadow_clean)

    # Launch FFmpeg process with piped input
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
        OUT_MP4
    ]

    print(f"Starting master encoding pipeline to {OUT_MP4}...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    t_start = time.time()
    margin_x = 64
    content_w = 1080 - 2 * margin_x

    for f_idx in range(TOTAL_FRAMES):
        t_sec = f_idx / float(FPS)

        # 1. Background Selection & Transition
        # Frame 0 to 160: Tabletop (0 to 5.33s)
        # Frame 160 to 220: Transition Tabletop -> Clean Stage (5.33s to 7.33s)
        # Frame 220 to 1590: Clean Technical Stage
        # Frame 1590 to 1678: Transition Clean -> Tabletop (53s to 56s loop)
        if f_idx < 160:
            frame_canvas = bg_table.copy()
        elif 160 <= f_idx < 220:
            prog = (f_idx - 160) / 60.0
            frame_canvas = bg_table.copy()
            clean_part = bg_clean.copy()
            # Alpha blend transition
            clean_part.putalpha(int(255 * prog))
            frame_canvas.alpha_composite(clean_part)
        elif 220 <= f_idx < 1590:
            frame_canvas = bg_clean.copy()
        else:
            prog = (f_idx - 1590) / 88.0
            frame_canvas = bg_clean.copy()
            table_part = bg_table.copy()
            table_part.putalpha(int(255 * prog))
            frame_canvas.alpha_composite(table_part)

        # 2. 3D Model Layer Animation
        if f_idx < 160:
            # Hero 3-Quarter Orbit & Subtle Scale
            zoom = 0.98 + 0.02 * ease_in_out(min(1.0, f_idx / 160.0))
            w_scaled = int(1080 * zoom)
            h_scaled = int(1920 * zoom)
            x_off = (1080 - w_scaled) // 2
            y_off = (1920 - h_scaled) // 2
            scaled_hero = img_hero.resize((w_scaled, h_scaled), Image.Resampling.BILINEAR)
            frame_canvas.alpha_composite(scaled_hero, (x_off, y_off))
        elif 160 <= f_idx < 240:
            # Slicing Split Animation
            prog = (f_idx - 160) / 80.0
            split_dx = int(160 * ease_out_quint(prog))
            cutaway_zoom = 0.92 + 0.08 * ease_out_cubic(prog)

            # Left half split of hero
            w_h = 540
            crop_l = img_hero.crop((0, 0, w_h, 1920))
            frame_canvas.alpha_composite(crop_l, (-split_dx, 0))

            # Right half split of hero
            crop_r = img_hero.crop((w_h, 0, 1080, 1920))
            frame_canvas.alpha_composite(crop_r, (w_h + split_dx, 0))

            # Cutaway appears from center
            cut_w = int(1080 * cutaway_zoom)
            cut_h = int(1920 * cutaway_zoom)
            cx_off = (1080 - cut_w) // 2
            cy_off = (1920 - cut_h) // 2
            scaled_cut = img_cutaway.resize((cut_w, cut_h), Image.Resampling.BILINEAR)
            # Fade in cutaway
            cut_alpha = scaled_cut.copy()
            cut_alpha.putalpha(int(255 * ease_out_cubic(prog)))
            frame_canvas.alpha_composite(cut_alpha, (cx_off, cy_off))
        elif 240 <= f_idx < 1590:
            # Frontal Cutaway Held Pose
            frame_canvas.alpha_composite(img_cutaway)
        else:
            # Snap Close back to Hero pose
            prog = (f_idx - 1590) / 88.0
            split_dx = int(160 * (1.0 - ease_out_cubic(prog)))
            w_h = 540
            crop_l = img_hero.crop((0, 0, w_h, 1920))
            frame_canvas.alpha_composite(crop_l, (-split_dx, 0))
            crop_r = img_hero.crop((w_h, 0, 1080, 1920))
            frame_canvas.alpha_composite(crop_r, (w_h + split_dx, 0))

        # Re-acquire draw context
        draw = ImageDraw.Draw(frame_canvas)

        # 3. Dynamic Thermal Waves & Particles (Active during Cue 07 & 08: 20s to 32s | frame 600 to 960)
        if 600 <= f_idx < 960:
            wave_phase = (f_idx - 600) * 0.25
            center_x = 540
            for y_base in [820, 920, 1020, 1120, 1200]:
                for i, offset_base in enumerate([40, 80, 120]):
                    osc = math.sin(wave_phase + i * 1.2 + y_base * 0.01) * 8
                    rad_x = offset_base + osc
                    draw.arc([center_x - rad_x, y_base - 26, center_x + rad_x, y_base + 26], start=300, end=420, fill=HEAT_ORANGE, width=2)
                # Bouncing reflection ray
                ref_x = 684
                bounce_len = 50 + int(math.sin(wave_phase + y_base) * 6)
                draw.line([(ref_x, y_base), (ref_x - bounce_len, y_base - 22)], fill=ELECTRIC, width=3)
                draw.polygon([(ref_x - bounce_len, y_base - 22), (ref_x - bounce_len + 12, y_base - 27), (ref_x - bounce_len + 8, y_base - 16)], fill=INK)

            # Pulsing heat packets
            for i, (px, py) in enumerate([(580, 850), (620, 880), (655, 910), (595, 950), (635, 990), (590, 1050), (630, 1080), (660, 1110)]):
                p_x_dyn = px + int(math.sin(wave_phase + i) * 6)
                p_y_dyn = py + int(math.cos(wave_phase + i * 0.8) * 4)
                draw.rectangle([p_x_dyn - 3, p_y_dyn - 3, p_x_dyn + 3, p_y_dyn + 3], fill=ELECTRIC, outline=INK, width=1)

        # 4. Kinetic SFX Pop-up ("KLIK!") at Stopper (Frame 110 to 145 | 3.68s - 4.8s)
        if 110 <= f_idx < 145:
            sfx_prog = (f_idx - 110) / 35.0
            if sfx_prog < 0.3:
                scale_sfx = 0.5 + 0.6 * ease_out_cubic(sfx_prog / 0.3)
            elif sfx_prog < 0.7:
                scale_sfx = 1.1 - 0.1 * ((sfx_prog - 0.3) / 0.4)
            else:
                scale_sfx = 1.0 - 0.8 * ((sfx_prog - 0.7) / 0.3)
            
            sfx_w = int(120 * scale_sfx)
            sfx_h = int(46 * scale_sfx)
            sx = 630 - sfx_w // 2
            sy = 450 - sfx_h // 2
            if sfx_w > 10 and sfx_h > 10:
                draw.rectangle([sx, sy, sx + sfx_w, sy + sfx_h], fill=POSITIVE, outline=INK, width=2)
                draw.text((sx + sfx_w // 2 - 28, sy + sfx_h // 2 - 14), "KLIK!", font=font_sfx, fill=PAPER)

        # 5. Header Zone (Slides in frame 0-25)
        head_prog = min(1.0, f_idx / 25.0)
        head_y_off = int(-100 * (1.0 - ease_out_cubic(head_prog)))
        draw.rectangle([margin_x, 70 + head_y_off, margin_x + 160, 94 + head_y_off], fill=WASH, outline=LINE, width=1)
        draw.text((margin_x + 10, 74 + head_y_off), "@porotheexplorer", font=font_eyebrow, fill=INK)
        draw.text((margin_x, 106 + head_y_off), "KENAPA TERMOS BISA TAHAN PANAS?", font=font_title, fill=INK)
        draw.line([(margin_x, 174 + head_y_off), (margin_x + content_w, 174 + head_y_off)], fill=INK, width=2)

        # 6. HUD Callouts Timing
        # HUD 02 (Celah Vakum): Active frame 240 to 611 (8.0s - 20.4s)
        if 240 <= f_idx < 611:
            hud_prog = min(1.0, (f_idx - 240) / 20.0)
            if f_idx > 585:
                hud_prog = max(0.0, (611 - f_idx) / 26.0)
            draw_hud_box(
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
                align_right=True,
                alpha_progress=hud_prog
            )

        # HUD 03 (Lapisan Emas): Active frame 611 to 914 (20.4s - 30.5s)
        if 611 <= f_idx < 914:
            hud_prog = min(1.0, (f_idx - 611) / 20.0)
            if f_idx > 885:
                hud_prog = max(0.0, (914 - f_idx) / 29.0)
            draw_hud_box(
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
                align_right=False,
                alpha_progress=hud_prog
            )

        # HUD 01 (Stopper Silikon): Active frame 914 to 1294 (30.5s - 43.1s)
        if 914 <= f_idx < 1294:
            hud_prog = min(1.0, (f_idx - 914) / 20.0)
            if f_idx > 1265:
                hud_prog = max(0.0, (1294 - f_idx) / 29.0)
            draw_hud_box(
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
                align_right=False,
                alpha_progress=hud_prog
            )

        # 7. C02 Metric Card (Slide-up spring entrance at Cue 12: 43.1s to 53.1s | frame 1294 to 1593)
        if 1294 <= f_idx < 1593:
            card_prog = min(1.0, (f_idx - 1294) / 25.0)
            if f_idx > 1565:
                card_prog = max(0.0, (1593 - f_idx) / 28.0)
            card_y = int(1950 - 420 * spring_val(card_prog))
            card_h = 245

            # Outer border
            draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + card_h], fill=PAPER, outline=INK, width=2)
            # Banner
            draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + 36], fill=INK)
            draw.text((margin_x + 16, card_y + 10), "P05 EVIDENCE / DATA RESMI ZOJIRUSHI CORPORATION", font=font_tag, fill=PAPER)

            # Left Col Wash
            div_x = margin_x + 295
            draw.rectangle([margin_x, card_y + 36, div_x, card_y + card_h], fill=WASH)
            draw.line([(div_x, card_y + 36), (div_x, card_y + card_h)], fill=INK, width=2)

            metric_x = margin_x + 28
            metric_y = card_y + 54
            draw.text((metric_x, metric_y), "≥71°C", font=font_metric_big, fill=INK)
            draw.text((metric_x + 4, metric_y + 80), "RETENSI 6 JAM", font=font_metric_label, fill=INK)
            draw.text((metric_x + 4, metric_y + 112), "Suhu Cairan Minimum", font=font_tag, fill=MUTED)

            # Right Col
            ctx_x = div_x + 24
            draw.text((ctx_x, card_y + 54), "Suhu Awal Uji: 95°C ±1°C | Suhu Ruang: 20°C ±2°C", font=font_body_bold, fill=INK)
            draw.text((ctx_x, card_y + 88), "Hasil akhir retensi panas setelah 6 jam pada posisi tegak.", font=font_body, fill=MUTED)
            draw.text((ctx_x, card_y + 118), "Spesifikasi resmi produsen Zojirushi Corporation (SM-WA48 / 480 ml).", font=font_body, fill=MUTED)

            pill_w = 345
            pill_h = 28
            pill_y = card_y + 154
            draw.rectangle([ctx_x, pill_y, ctx_x + pill_w, pill_y + pill_h], fill=POSITIVE)
            draw.text((ctx_x + 14, pill_y + 6), "STATUS: FAKTA TERVERIFIKASI (KLAIM RESMI)", font=font_badge, fill=PAPER)

            badge2_x = ctx_x + pill_w + 12
            badge2_w = 120
            draw.rectangle([badge2_x, pill_y, badge2_x + badge2_w, pill_y + pill_h], fill=INFO)
            draw.text((badge2_x + 12, pill_y + 6), "STANDAR JIS", font=font_badge, fill=PAPER)

        # 8. Dynamic Subtitle Karaoke (Locked at Y=1380, Center-Aligned at X=540, Max 4 Words)
        # Find active chunk
        active_chunk = None
        for c in chunks:
            if c[0]["start"] <= t_sec <= c[-1]["end"] + 0.35:
                active_chunk = c
                break

        if active_chunk:
            sub_y = 1380
            # Pre-calculate widths
            word_boxes = []
            pad_h_x = 10
            pad_h_y = 6
            total_w = 0

            for w_item in active_chunk:
                is_active = (w_item["start"] <= t_sec <= w_item["end"])
                f_used = font_subtitle_bold if is_active else font_subtitle
                bbox = draw.textbbox((0, 0), w_item["word"], font=f_used)
                ww = bbox[2] - bbox[0]
                word_boxes.append({
                    "word": w_item["word"],
                    "is_active": is_active,
                    "w": ww,
                    "h": bbox[3] - bbox[1],
                    "font": f_used
                })
                total_w += ww + (2 * pad_h_x if is_active else 0) + 12  # 12px space

            total_w -= 12
            start_x = (1080 - total_w) // 2

            # Timing Pill
            cue_text = f"AUDIO CUE: {int(t_sec//60):02d}:{t_sec%60:06.3f}"
            c_bbox = draw.textbbox((0, 0), cue_text, font=font_tag)
            c_w = c_bbox[2] - c_bbox[0]
            cx = (1080 - c_w) // 2
            draw.rectangle([cx - 12, sub_y - 42, cx + c_w + 12, sub_y - 18], fill=WASH, outline=LINE, width=1)
            draw.text((cx, sub_y - 38), cue_text, font=font_tag, fill=INK)

            # Draw Words
            cur_x = start_x
            for wb in word_boxes:
                if wb["is_active"]:
                    b_l = cur_x
                    b_t = sub_y - pad_h_y
                    b_r = cur_x + wb["w"] + 2 * pad_h_x
                    b_b = sub_y + wb["h"] + pad_h_y
                    draw.rectangle([b_l, b_t, b_r, b_b], fill=ELECTRIC, outline=INK, width=2)
                    draw.text((cur_x + pad_h_x, sub_y), wb["word"], font=wb["font"], fill=INK)
                    cur_x = b_r + 12
                else:
                    draw.text((cur_x, sub_y), wb["word"], font=wb["font"], fill=INK)
                    cur_x += wb["w"] + 12

        # Pipe raw RGBA frame to FFmpeg
        proc.stdin.write(frame_canvas.tobytes())

        if f_idx % 150 == 0:
            elapsed = time.time() - t_start
            fps_actual = (f_idx + 1) / elapsed if elapsed > 0 else 0
            print(f"Rendered frame {f_idx:4d}/{TOTAL_FRAMES} ({f_idx/TOTAL_FRAMES*100:4.1f}%) at {fps_actual:5.1f} fps")

    proc.stdin.close()
    proc.wait()
    t_end = time.time()
    print(f"Master animation assembled and encoded in {t_end - t_start:.2f} seconds!")
    print(f"Output saved to: {OUT_MP4}")


if __name__ == "__main__":
    render_video()
