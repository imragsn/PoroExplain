"""
Master Video Animation Assembly v0.2
Fixes all user feedback:
1. Dynamic Camera & Shot Variety: Uses all 4 3D transparent angles rendered from Blender:
   - Shot 01: Hero 3-Quarter (0.0s - 5.3s) on Tabletop with orbit & open
   - Shot 02: Frontal Cross-Section 5-Layers (5.3s - 20.4s) with push-in dolly to vacuum gap
   - Shot 03: Isometric 3D Wedge Cut (20.4s - 30.5s) showing 3D depth of gold reflective wall
   - Shot 04: Macro Close-Up Neck & Silicone Stopper (30.5s - 43.1s)
   - Shot 05: Frontal Technical View with C02 Metric Evidence Card (43.1s - 53.1s)
   - Shot 06: Snap-Close & Pull-Out Outro Loop (53.1s - 55.97s)
2. Upgraded Mobile Readability:
   - HUD Tags: 16px Bold
   - HUD Titles: 28px Bold
   - HUD Body: 20px Regular/Medium
   - Metric Big Number: 84px Bold (≥71°C)
   - Metric Label: 26px Bold
   - Context lines: 22px Bold / 19px Regular
3. Zero-Latency Subtitle Karaoke:
   - Frame-accurate millisecond synchronization, no delay buffer.
   - Max 4 words per chunk, center-aligned at X=540, Y=1380.
   - Active word highlighted in Electric Yellow (#E8F500) box with 2px ink stroke.
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

SHOT_01_HERO = os.path.join(ROOT, "work", "termos-3d", "shot_01_hero_trans.png")
SHOT_02_CUTAWAY = os.path.join(ROOT, "work", "termos-3d", "shot_02_cutaway_trans.png")
SHOT_03_STOPPER = os.path.join(ROOT, "work", "termos-3d", "shot_03_stopper_trans.png")
SHOT_04_ISOWEDGE = os.path.join(ROOT, "work", "termos-3d", "shot_04_isowedges_trans.png")

OUT_MP4 = os.path.join(OUTPUTS_DIR, "termos-06-animasi-master-v0.2.mp4")

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
HEAT_ORANGE = (230, 110, 25, 220)

FPS = 30
TOTAL_DURATION = 55.968
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)  # 1679 frames


def get_font(size, weight=400):
    f = ImageFont.truetype(FONT_PATH, size)
    f.set_variation_by_axes([weight])
    return f


font_title = get_font(46, 700)
font_eyebrow = get_font(18, 600)
font_hud_tag = get_font(16, 700)
font_hud_title = get_font(28, 700)
font_hud_body = get_font(20, 400)
font_subtitle = get_font(42, 400)
font_subtitle_bold = get_font(42, 700)
font_metric_big = get_font(84, 700)
font_metric_lbl = get_font(26, 700)
font_ctx_bold = get_font(22, 700)
font_ctx_reg = get_font(19, 400)
font_badge = get_font(16, 700)
font_sfx = get_font(26, 700)


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


def get_subtitle_at_time(chunks, t):
    """Zero-latency frame-accurate subtitle lookup."""
    for i, c in enumerate(chunks):
        t0 = c[0]["start"]
        t1 = chunks[i+1][0]["start"] if i+1 < len(chunks) else c[-1]["end"] + 0.5
        if t0 <= t < t1:
            act = [w for w in c if w["start"] <= t < w["end"]]
            return c, (act[0] if act else None)
    return None, None


def draw_hud_box(draw, x_anchor, y_anchor, x_box, y_box, w_box, h_box, tag, title, body_lines, accent_color, align_right=False, alpha_prog=1.0):
    if alpha_prog <= 0.01:
        return

    scale = 0.88 + 0.12 * ease_out_cubic(alpha_prog)
    cur_w = int(w_box * scale)
    cur_h = int(h_box * scale)
    y_connect = y_box + cur_h // 2

    if align_right:
        x_connect = x_box + cur_w
        elbow_x = (x_connect + x_anchor) // 2
        line_prog = min(1.0, alpha_prog * 1.5)
        p1 = (x_anchor, y_anchor)
        p2 = (int(x_anchor + (elbow_x - x_anchor) * line_prog), y_anchor)
        draw.line([p1, p2], fill=INK, width=2)
        if line_prog > 0.5:
            lp2 = (line_prog - 0.5) / 0.5
            p3 = (elbow_x, int(y_anchor + (y_connect - y_anchor) * lp2))
            draw.line([p2, p3], fill=INK, width=2)
            p4 = (int(elbow_x + (x_connect - elbow_x) * lp2), y_connect)
            draw.line([p3, p4], fill=INK, width=2)
    else:
        x_connect = x_box
        elbow_x = (x_anchor + x_connect) // 2
        line_prog = min(1.0, alpha_prog * 1.5)
        p1 = (x_anchor, y_anchor)
        p2 = (int(x_anchor + (elbow_x - x_anchor) * line_prog), y_anchor)
        draw.line([p1, p2], fill=INK, width=2)
        if line_prog > 0.5:
            lp2 = (line_prog - 0.5) / 0.5
            p3 = (elbow_x, int(y_anchor + (y_connect - y_anchor) * lp2))
            draw.line([p2, p3], fill=INK, width=2)
            p4 = (int(elbow_x + (x_connect - elbow_x) * lp2), y_connect)
            draw.line([p3, p4], fill=INK, width=2)

    # Pin point at anchor
    draw.rectangle([x_anchor - 5, y_anchor - 5, x_anchor + 5, y_anchor + 5], fill=accent_color, outline=INK, width=2)

    if alpha_prog > 0.15:
        # Sharp zero-radius box with paper background
        draw.rectangle([x_box, y_box, x_box + cur_w, y_box + cur_h], fill=PAPER, outline=INK, width=2)
        header_h = 32
        draw.rectangle([x_box, y_box, x_box + cur_w, y_box + header_h], fill=accent_color)
        draw.text((x_box + 16, y_box + 6), tag.upper(), font=font_hud_tag, fill=PAPER)

        pad_x = 20
        draw.text((x_box + pad_x, y_box + 44), title.upper(), font=font_hud_title, fill=INK)

        line_y = y_box + 86
        for line in body_lines:
            draw.text((x_box + pad_x, line_y), line, font=font_hud_body, fill=MUTED)
            line_y += 30


def apply_camera_transform(img, scale=1.0, pan_x=0, pan_y=0):
    if math.isclose(scale, 1.0, abs_tol=1e-3) and pan_x == 0 and pan_y == 0:
        return img
    w, h = img.size
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = img.resize((new_w, new_h), Image.Resampling.BILINEAR)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x_pos = (w - new_w) // 2 + pan_x
    y_pos = (h - new_h) // 2 + pan_y
    canvas.alpha_composite(resized, (x_pos, y_pos))
    return canvas


def assemble_master_video():
    print("Loading master audio & cues...")
    words = parse_srt(SRT_FILE)
    chunks = build_subtitle_chunks(words)
    print(f"Loaded {len(words)} words into {len(chunks)} subtitle chunks.")

    print("Loading 4 transparent 3D master shots from Blender...")
    img_shot1 = Image.open(SHOT_01_HERO).convert("RGBA")
    img_shot2 = Image.open(SHOT_02_CUTAWAY).convert("RGBA")
    img_shot3 = Image.open(SHOT_03_STOPPER).convert("RGBA")
    img_shot4 = Image.open(SHOT_04_ISOWEDGE).convert("RGBA")

    # Tabletop background
    bg_table = Image.new("RGBA", (1080, 1920), PAPER)
    d_tab = ImageDraw.Draw(bg_table)
    for y in range(1220):
        r = int(252 - (y / 1220) * 8)
        g = int(250 - (y / 1220) * 9)
        b = int(246 - (y / 1220) * 12)
        d_tab.line([(0, y), (1080, y)], fill=(r, g, b, 255))
    d_tab.rectangle([0, 1220, 1080, 1920], fill=(238, 232, 222, 255))
    d_tab.line([(0, 1220), (1080, 1220)], fill=(215, 208, 196, 255), width=2)
    d_tab.line([(0, 1222), (1080, 1222)], fill=(248, 245, 240, 255), width=1)

    s_tab = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    st_draw = ImageDraw.Draw(s_tab)
    st_draw.ellipse([340, 1238, 740, 1262], fill=(60, 50, 40, 90))
    st_draw.ellipse([360, 1242, 720, 1258], fill=(40, 30, 20, 140))
    s_tab = s_tab.filter(ImageFilter.GaussianBlur(radius=8))
    bg_table.alpha_composite(s_tab)

    # Clean Studio background
    bg_clean = Image.new("RGBA", (1080, 1920), PAPER)
    s_clean = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    sc_draw = ImageDraw.Draw(s_clean)
    sc_draw.ellipse([330, 1238, 750, 1262], fill=(16, 17, 16, 45))
    sc_draw.ellipse([360, 1242, 720, 1258], fill=(16, 17, 16, 75))
    s_clean = s_clean.filter(ImageFilter.GaussianBlur(radius=7))
    bg_clean.alpha_composite(s_clean)

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

    print(f"Launching master encoding to {OUT_MP4}...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    t_start = time.time()

    margin_x = 54
    content_w = 1080 - 2 * margin_x

    for f_idx in range(TOTAL_FRAMES):
        t_sec = f_idx / float(FPS)

        # ----------------------------------------------------
        # 1. Background Environment Transition
        # ----------------------------------------------------
        if f_idx < 160:
            frame_canvas = bg_table.copy()
        elif 160 <= f_idx < 220:
            prog = (f_idx - 160) / 60.0
            frame_canvas = bg_table.copy()
            clean_part = bg_clean.copy()
            clean_part.putalpha(int(255 * prog))
            frame_canvas.alpha_composite(clean_part)
        elif 220 <= f_idx < 1590:
            frame_canvas = bg_clean.copy()
        else:
            prog = (f_idx - 1590) / 88.0
            frame_canvas = bg_clean.copy()
            tab_part = bg_table.copy()
            tab_part.putalpha(int(255 * prog))
            frame_canvas.alpha_composite(tab_part)

        # ----------------------------------------------------
        # 2. Multi-Angle 3D Camera & Model Movement Choreography
        # ----------------------------------------------------
        # Shot 1: Hero Orbit & Zoom (0 to 160 | 0.0s - 5.3s)
        if f_idx < 160:
            cam_scale = 0.95 + 0.07 * ease_in_out(f_idx / 160.0)
            pan_x = int(-15 * math.sin((f_idx / 160.0) * math.pi))
            shot_rendered = apply_camera_transform(img_shot1, scale=cam_scale, pan_x=pan_x, pan_y=0)
            frame_canvas.alpha_composite(shot_rendered)

        # Shot 2: Split Transition & Frontal Cutaway Push-In (160 to 611 | 5.3s - 20.4s)
        elif 160 <= f_idx < 611:
            if f_idx < 240:
                prog = (f_idx - 160) / 80.0
                split_dx = int(180 * ease_out_quint(prog))
                # Left half split of hero
                crop_l = img_shot1.crop((0, 0, 540, 1920))
                frame_canvas.alpha_composite(crop_l, (-split_dx, 0))
                # Right half split of hero
                crop_r = img_shot1.crop((540, 0, 1080, 1920))
                frame_canvas.alpha_composite(crop_r, (540 + split_dx, 0))
                # Fade-in cutaway
                cut_alpha = img_shot2.copy()
                cut_alpha.putalpha(int(255 * ease_out_cubic(prog)))
                frame_canvas.alpha_composite(cut_alpha)
            else:
                # Camera push-in towards vacuum gap
                prog = min(1.0, (f_idx - 240) / 370.0)
                cam_scale = 1.0 + 0.12 * ease_out_cubic(prog)
                pan_x = int(-25 * ease_out_cubic(prog))  # Pan toward left vacuum gap
                shot_rendered = apply_camera_transform(img_shot2, scale=cam_scale, pan_x=pan_x, pan_y=0)
                frame_canvas.alpha_composite(shot_rendered)

        # Shot 3: CUT TO Isometric 3D Wedge Cut (611 to 914 | 20.4s - 30.5s)
        elif 611 <= f_idx < 914:
            prog = (f_idx - 611) / 303.0
            cam_scale = 1.02 + 0.04 * math.sin(prog * math.pi)
            pan_x = int(12 * math.cos(prog * math.pi))
            shot_rendered = apply_camera_transform(img_shot4, scale=cam_scale, pan_x=pan_x, pan_y=0)
            frame_canvas.alpha_composite(shot_rendered)

        # Shot 4: CUT TO Macro Close-Up Neck & Silicone Stopper (914 to 1294 | 30.5s - 43.1s)
        elif 914 <= f_idx < 1294:
            prog = (f_idx - 914) / 380.0
            cam_scale = 1.03 + 0.05 * ease_in_out(prog)
            pan_y = int(20 * math.sin(prog * math.pi))
            shot_rendered = apply_camera_transform(img_shot3, scale=cam_scale, pan_x=0, pan_y=pan_y)
            frame_canvas.alpha_composite(shot_rendered)

        # Shot 5: Return to Frontal Cross-Section for Metric Proof (1294 to 1590 | 43.1s - 53.0s)
        elif 1294 <= f_idx < 1590:
            frame_canvas.alpha_composite(img_shot2)

        # Shot 6: Snap-Close & Pull-Out Outro Loop (1590 to 1678 | 53.0s - 55.97s)
        else:
            prog = (f_idx - 1590) / 88.0
            split_dx = int(180 * (1.0 - ease_out_cubic(prog)))
            crop_l = img_shot1.crop((0, 0, 540, 1920))
            frame_canvas.alpha_composite(crop_l, (-split_dx, 0))
            crop_r = img_shot1.crop((540, 0, 1080, 1920))
            frame_canvas.alpha_composite(crop_r, (540 + split_dx, 0))

        draw = ImageDraw.Draw(frame_canvas)

        # ----------------------------------------------------
        # 3. Dynamic Visual Effects: Thermal Radiation & Steam
        # ----------------------------------------------------
        # Kinetic Pop-up "KLIK!" at stopper (Frame 110 to 145)
        if 110 <= f_idx < 145:
            sfx_prog = (f_idx - 110) / 35.0
            scale_sfx = 0.6 + 0.5 * spring_val(sfx_prog, damping=12, stiffness=140) if sfx_prog < 0.7 else 1.1 - (sfx_prog - 0.7) * 3
            sw = int(130 * scale_sfx)
            sh = int(50 * scale_sfx)
            sx = 640 - sw // 2
            sy = 450 - sh // 2
            if sw > 10 and sh > 10:
                draw.rectangle([sx, sy, sx + sw, sy + sh], fill=POSITIVE, outline=INK, width=2)
                draw.text((sx + sw // 2 - 32, sy + sh // 2 - 15), "KLIK!", font=font_sfx, fill=PAPER)

        # Steam Wisps (Frame 115 to 160)
        if 115 <= f_idx < 160:
            sp = (f_idx - 115) / 45.0
            for si in range(3):
                y_wisp = int(480 - sp * 140 - si * 25)
                x_wisp = int(540 + math.sin(sp * 8 + si * 2) * 18)
                rad = int(8 + sp * 18)
                alpha_wisp = int(80 * (1.0 - sp))
                draw.ellipse([x_wisp - rad, y_wisp - rad // 2, x_wisp + rad, y_wisp + rad // 2], outline=(150, 150, 150, alpha_wisp), width=2)

        # Thermal Infrared Waves & Particles in Shot 3 (Isometric View, Frame 611 to 914)
        if 611 <= f_idx < 914:
            phase = (f_idx - 611) * 0.28
            cx = 540
            for yb in [810, 910, 1010, 1110, 1200]:
                for i, r_base in enumerate([45, 90, 135]):
                    r_dyn = r_base + math.sin(phase + i * 1.3) * 10
                    draw.arc([cx - r_dyn, yb - 28, cx + r_dyn, yb + 28], start=290, end=430, fill=HEAT_ORANGE, width=3)
                # Reflection ray
                draw.line([(680, yb), (620, yb - 25)], fill=ELECTRIC, width=3)
                draw.polygon([(620, yb - 25), (634, yb - 30), (630, yb - 18)], fill=INK)

            for i, (px, py) in enumerate([(580, 840), (620, 875), (660, 910), (595, 950), (640, 990), (590, 1050), (635, 1085)]):
                p_xd = px + int(math.sin(phase + i) * 8)
                p_yd = py + int(math.cos(phase + i * 0.9) * 5)
                draw.rectangle([p_xd - 4, p_yd - 4, p_xd + 4, p_yd + 4], fill=ELECTRIC, outline=INK, width=2)

        # ----------------------------------------------------
        # 4. VOLT DS Header Zone (Slides in Frame 0 to 25)
        # ----------------------------------------------------
        head_prog = min(1.0, f_idx / 25.0)
        head_y_off = int(-110 * (1.0 - ease_out_cubic(head_prog)))
        draw.rectangle([margin_x, 68 + head_y_off, margin_x + 180, 96 + head_y_off], fill=WASH, outline=LINE, width=1)
        draw.text((margin_x + 12, 72 + head_y_off), "@porotheexplorer", font=font_eyebrow, fill=INK)
        draw.text((margin_x, 106 + head_y_off), "KENAPA TERMOS BISA TAHAN PANAS?", font=font_title, fill=INK)
        draw.line([(margin_x, 176 + head_y_off), (margin_x + content_w, 176 + head_y_off)], fill=INK, width=2)

        # ----------------------------------------------------
        # 5. Upgraded Mobile HUD Callouts (20px Body / 28px Titles)
        # ----------------------------------------------------
        # HUD 02 (Celah Vakum): Active Frame 336 to 611 (11.2s - 20.4s)
        if 336 <= f_idx < 611:
            h_prog = min(1.0, (f_idx - 336) / 22.0)
            if f_idx > 585:
                h_prog = max(0.0, (611 - f_idx) / 26.0)
            draw_hud_box(
                draw,
                x_anchor=380, y_anchor=970,
                x_box=margin_x, y_box=890,
                w_box=345, h_box=160,
                tag="02 / ISOLASI FISIKA",
                title="Celah Vakum",
                body_lines=[
                    "Ruang hampa ~2mm memutus",
                    "jalur konduksi & konveksi."
                ],
                accent_color=INFO,
                align_right=True,
                alpha_prog=h_prog
            )

        # HUD 03 (Lapisan Emas): Active Frame 611 to 914 (20.4s - 30.5s)
        if 611 <= f_idx < 914:
            h_prog = min(1.0, (f_idx - 611) / 22.0)
            if f_idx > 885:
                h_prog = max(0.0, (914 - f_idx) / 29.0)
            draw_hud_box(
                draw,
                x_anchor=660, y_anchor=880,
                x_box=680, y_box=790,
                w_box=345, h_box=160,
                tag="03 / RADIASI PANAS",
                title="Lapisan Emas",
                body_lines=[
                    "Memantulkan gelombang",
                    "inframerah balik ke air."
                ],
                accent_color=AMBER,
                align_right=False,
                alpha_prog=h_prog
            )

        # HUD 01 (Stopper Silikon): Active Frame 914 to 1294 (30.5s - 43.1s)
        if 914 <= f_idx < 1294:
            h_prog = min(1.0, (f_idx - 914) / 22.0)
            if f_idx > 1265:
                h_prog = max(0.0, (1294 - f_idx) / 29.0)
            draw_hud_box(
                draw,
                x_anchor=560, y_anchor=520,
                x_box=680, y_box=420,
                w_box=345, h_box=160,
                tag="01 / BUKAAN KEDAP",
                title="Stopper Silikon",
                body_lines=[
                    "Sumbat 4,0 cm mengunci uap",
                    "panas agar tidak konveksi."
                ],
                accent_color=POSITIVE,
                align_right=False,
                alpha_prog=h_prog
            )

        # ----------------------------------------------------
        # 6. C02 Metric Evidence Card (Frame 1294 to 1590 | 43.1s - 53.0s)
        # ----------------------------------------------------
        if 1294 <= f_idx < 1590:
            c_prog = min(1.0, (f_idx - 1294) / 25.0)
            if f_idx > 1560:
                c_prog = max(0.0, (1590 - f_idx) / 30.0)
            card_y = int(1950 - 450 * spring_val(c_prog))
            card_h = 270

            draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + card_h], fill=PAPER, outline=INK, width=2)
            # Top Banner
            draw.rectangle([margin_x, card_y, margin_x + content_w, card_y + 40], fill=INK)
            draw.text((margin_x + 18, card_y + 10), "P05 EVIDENCE / DATA RESMI ZOJIRUSHI CORPORATION", font=font_hud_tag, fill=PAPER)

            # Left Column (Wash Tint)
            div_x = margin_x + 310
            draw.rectangle([margin_x, card_y + 40, div_x, card_y + card_h], fill=WASH)
            draw.line([(div_x, card_y + 40), (div_x, card_y + card_h)], fill=INK, width=2)

            metric_x = margin_x + 28
            draw.text((metric_x, card_y + 54), "≥71°C", font=font_metric_big, fill=INK)
            draw.text((metric_x + 4, card_y + 155), "RETENSI 6 JAM", font=font_metric_lbl, fill=INK)
            draw.text((metric_x + 4, card_y + 195), "Suhu Cairan Minimum", font=font_hud_tag, fill=MUTED)

            # Right Column
            ctx_x = div_x + 24
            draw.text((ctx_x, card_y + 58), "Suhu Awal Uji: 95°C ±1°C | Suhu Ruang: 20°C ±2°C", font=font_ctx_bold, fill=INK)
            draw.text((ctx_x, card_y + 98), "Hasil akhir retensi panas setelah 6 jam pada posisi tegak.", font=font_ctx_reg, fill=MUTED)
            draw.text((ctx_x, card_y + 134), "Spesifikasi resmi produsen Zojirushi Corporation (SM-WA48 / 480 ml).", font=font_ctx_reg, fill=MUTED)

            pill_w = 370
            pill_h = 34
            pill_y = card_y + 182
            draw.rectangle([ctx_x, pill_y, ctx_x + pill_w, pill_y + pill_h], fill=POSITIVE)
            draw.text((ctx_x + 16, pill_y + 7), "STATUS: FAKTA TERVERIFIKASI (KLAIM RESMI)", font=font_badge, fill=PAPER)

            badge2_x = ctx_x + pill_w + 14
            badge2_w = 140
            draw.rectangle([badge2_x, pill_y, badge2_x + badge2_w, pill_y + pill_h], fill=INFO)
            draw.text((badge2_x + 16, pill_y + 7), "STANDAR JIS", font=font_badge, fill=PAPER)

        # ----------------------------------------------------
        # 7. Zero-Latency Subtitle Karaoke Engine
        # ----------------------------------------------------
        active_chunk, active_w = get_subtitle_at_time(chunks, t_sec)

        if active_chunk:
            sub_y = 1380
            word_boxes = []
            pad_h_x = 12
            pad_h_y = 8
            total_w = 0

            for w_item in active_chunk:
                is_active = (active_w is not None and w_item["id"] == active_w["id"])
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
                total_w += ww + (2 * pad_h_x if is_active else 0) + 14

            total_w -= 14
            start_x = (1080 - total_w) // 2

            # Timing Pill
            cue_text = f"AUDIO CUE: {int(t_sec//60):02d}:{t_sec%60:06.3f}"
            c_bbox = draw.textbbox((0, 0), cue_text, font=font_hud_tag)
            c_w = c_bbox[2] - c_bbox[0]
            cx = (1080 - c_w) // 2
            draw.rectangle([cx - 14, sub_y - 46, cx + c_w + 14, sub_y - 18], fill=WASH, outline=LINE, width=1)
            draw.text((cx, sub_y - 42), cue_text, font=font_hud_tag, fill=INK)

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
                    cur_x = b_r + 14
                else:
                    draw.text((cur_x, sub_y), wb["word"], font=wb["font"], fill=INK)
                    cur_x += wb["w"] + 14

        # Stream raw RGBA frame to FFmpeg pipe
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
    assemble_master_video()
