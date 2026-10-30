from PIL import Image, ImageDraw, ImageFont
import os


ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
RENDER_DIR = os.path.join(ROOT, "work", "termos-3d", "renders-v01")
REFERENCE = os.path.join(ROOT, "work", "termos-references", "sm-wa48-product.png")
OUTPUT = os.path.join(ROOT, "outputs", "termos-03-validasi-eksterior-v0.1.png")

W, H = 1800, 1280
BG = (239, 234, 224)
CARD = (249, 247, 241)
INK = (34, 38, 39)
MUTED = (88, 94, 94)
ACCENT = (229, 190, 48)
BORDER = (208, 202, 191)


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


F_TITLE = font(42, True)
F_SUB = font(21)
F_LABEL = font(23, True)
F_BODY = font(19)
F_SMALL = font(16)


def rounded_card(draw, box):
    draw.rounded_rectangle(box, radius=26, fill=CARD, outline=BORDER, width=2)


def contain(img, box, pad=24):
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0 - pad * 2, y1 - y0 - pad * 2
    scale = min(mw / img.width, mh / img.height)
    resized = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.Resampling.LANCZOS)
    px = x0 + (x1 - x0 - resized.width) // 2
    py = y0 + (y1 - y0 - resized.height) // 2
    return resized, (px, py)


def place_image(canvas, img, box, pad=24):
    fitted, pos = contain(img, box, pad)
    if fitted.mode == "RGBA":
        canvas.alpha_composite(fitted, pos)
    else:
        canvas.paste(fitted, pos)


canvas = Image.new("RGBA", (W, H), BG + (255,))
draw = ImageDraw.Draw(canvas)

draw.text((60, 42), "VALIDASI EKSTERIOR 3D — TERMOS SM-WA48", font=F_TITLE, fill=INK)
draw.text((62, 98), "Model produksi v0.1 • bentuk luar dahulu, bagian dalam belum dikunci", font=F_SUB, fill=MUTED)
draw.rounded_rectangle((1430, 46, 1740, 96), radius=22, fill=ACCENT)
draw.text((1488, 57), "CHECKPOINT USER", font=F_LABEL, fill=(30, 31, 30))

cards = {
    "reference": (50, 145, 580, 700),
    "front": (635, 145, 1165, 700),
    "three": (1220, 145, 1750, 700),
    "side": (50, 745, 580, 1215),
    "rear": (635, 745, 1165, 1215),
    "notes": (1220, 745, 1750, 1215),
}
for box in cards.values():
    rounded_card(draw, box)

draw.text((78, 166), "REFERENSI RESMI — DEPAN", font=F_LABEL, fill=INK)
draw.text((663, 166), "MODEL — DEPAN", font=F_LABEL, fill=INK)
draw.text((1248, 166), "MODEL — 3/4", font=F_LABEL, fill=INK)
draw.text((78, 766), "MODEL — SAMPING", font=F_LABEL, fill=INK)
draw.text((663, 766), "MODEL — 3/4 BELAKANG", font=F_LABEL, fill=INK)
draw.text((1248, 766), "STATUS AKURASI", font=F_LABEL, fill=INK)

source = Image.open(REFERENCE).convert("RGBA")
# The official composite is a 4×2 lineup; ice-gray is the lower-left cell.
ref_crop = source.crop((0, source.height // 2, source.width // 4 + 4, source.height))
place_image(canvas, ref_crop, (70, 205, 560, 676), pad=26)

render_map = {
    "front": (cards["front"], "front.png"),
    "three": (cards["three"], "three_quarter.png"),
    "side": (cards["side"], "side.png"),
    "rear": (cards["rear"], "rear_three_quarter.png"),
}
for _, (box, filename) in render_map.items():
    img = Image.open(os.path.join(RENDER_DIR, filename)).convert("RGBA")
    place_image(canvas, img, (box[0] + 12, box[1] + 55, box[2] - 12, box[3] - 15), pad=0)

notes = [
    ("DIMENSI TERKUNCI", "6,5 × 7 × 21,5 cm (≈, spesifikasi resmi)"),
    ("DEPAN", "Keyakinan menengah–tinggi: dibandingkan foto resmi."),
    ("TUTUP & KONTROL", "Keyakinan menengah: bentuk dasar dari foto tutup resmi."),
    ("SAMPING/BELAKANG", "Keyakinan menengah–rendah: belum ada foto ortografis resmi."),
    ("BATAS V0.1", "Logo placeholder; bagian dalam belum dibuat atau diklaim presisi."),
]
y = 815
for title, body in notes:
    draw.ellipse((1248, y + 4, 1262, y + 18), fill=ACCENT)
    draw.text((1276, y), title, font=F_SMALL, fill=INK)
    y += 23
    draw.multiline_text((1276, y), body, font=F_SMALL, fill=MUTED, spacing=4)
    y += 36

draw.rounded_rectangle((1248, 1110, 1722, 1184), radius=16, fill=(233, 228, 216))
draw.multiline_text(
    (1264, 1121),
    "Tujuan review: cek siluet, proporsi tutup, tombol,\nbahu, dan dasar sebelum membuat cutaway.",
    font=F_SMALL,
    fill=INK,
    spacing=4,
)

canvas.convert("RGB").save(OUTPUT, quality=96)
print(OUTPUT)
