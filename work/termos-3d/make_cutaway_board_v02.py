from PIL import Image, ImageDraw, ImageFont
import os
import textwrap


ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
R = os.path.join(ROOT, "work", "termos-3d", "renders-v02")
OUT = os.path.join(ROOT, "outputs", "termos-03-validasi-cutaway-v0.2.png")

W, H = 1800, 1120
BG = (239, 234, 224)
CARD = (249, 247, 241)
INK = (34, 38, 39)
MUTED = (87, 93, 93)
BORDER = (207, 201, 190)
YELLOW = (235, 188, 38)


def get_font(size, bold=False):
    path = r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"
    return ImageFont.truetype(path, size)


FT = get_font(40, True)
FS = get_font(20)
FL = get_font(22, True)
FB = get_font(17)
FBB = get_font(17, True)


def card(draw, box):
    draw.rounded_rectangle(box, radius=24, fill=CARD, outline=BORDER, width=2)


def fit(img, box, pad=12):
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0 - 2 * pad, y1 - y0 - 2 * pad
    scale = min(mw / img.width, mh / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
    return img, (x0 + (x1 - x0 - img.width) // 2, y0 + (y1 - y0 - img.height) // 2)


canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)
draw.text((58, 38), "VALIDASI CUTAWAY 3D — TERMOS", font=FT, fill=INK)
draw.text((60, 94), "Master v0.2 • geometri animatable, ukuran internal ditampilkan skematis", font=FS, fill=MUTED)
draw.rounded_rectangle((1450, 43, 1742, 93), radius=22, fill=YELLOW)
draw.text((1500, 55), "BUKTI DIPISAH", font=FL, fill=INK)

left = (48, 142, 610, 910)
middle = (634, 142, 1196, 910)
right = (1220, 142, 1752, 910)
for b in (left, middle, right):
    card(draw, b)

draw.text((76, 164), "CUTAWAY 3/4", font=FL, fill=INK)
draw.text((662, 164), "EXPLODED VIEW", font=FL, fill=INK)
draw.text((1248, 164), "STATUS PER KOMPONEN", font=FL, fill=INK)

for path, box in [
    (os.path.join(R, "cutaway_three_quarter.png"), (66, 208, 592, 890)),
    (os.path.join(R, "exploded_three_quarter.png"), (652, 208, 1178, 890)),
]:
    img = Image.open(path).convert("RGB")
    img, pos = fit(img, box, pad=0)
    canvas.paste(img, pos)

legend = [
    ((102, 125, 127), "DINDING LUAR", "Eksterior terukur; ketebalan internal skematis."),
    ((45, 151, 188), "CELAH VAKUM", "Prinsip terverifikasi; biru hanya marker batas ruang kosong."),
    ((238, 177, 35), "LAPISAN REFLEKTIF", "Prinsip umum terverifikasi; bahan/ketebalan model ini belum pasti."),
    ((120, 126, 128), "DINDING DALAM", "Struktur dinding ganda terverifikasi; profil detail skematis."),
    ((171, 46, 25), "AIR PANAS", "Isi ilustratif; tinggi permukaan bukan hasil pengukuran produk."),
    ((31, 34, 34), "GASKET & LEHER", "Keberadaan/jalur panas didukung; bentuk presisi belum terverifikasi."),
]
y = 212
for color, title, desc in legend:
    draw.rounded_rectangle((1248, y + 3, 1270, y + 25), radius=6, fill=color)
    draw.text((1285, y), title, font=FBB, fill=INK)
    y += 25
    wrapped = "\n".join(textwrap.wrap(desc, width=49))
    draw.multiline_text((1285, y), wrapped, font=FB, fill=MUTED, spacing=3)
    y += 69

draw.rounded_rectangle((1245, 726, 1728, 874), radius=18, fill=(234, 228, 215))
draw.text((1264, 746), "LARANGAN KLAIM", font=FBB, fill=INK)
draw.multiline_text(
    (1264, 778),
    "• ketebalan dinding persis\n• lebar celah vakum persis\n• material foil khusus SM-WA48\n• mekanisme tutup setara CAD pabrik",
    font=FB,
    fill=INK,
    spacing=7,
)

draw.rounded_rectangle((48, 942, 1752, 1068), radius=22, fill=(36, 41, 41))
draw.text((76, 964), "ATURAN PRODUKSI", font=FL, fill=(246, 243, 234))
rule_text = (
    "Akurasi dikunci pada siluet, urutan lapisan, dan hubungan sebab–akibat. Ketebalan internal diperbesar agar terbaca. "
    "Model yang sama akan menggerakkan cutaway, label, kamera, dan exploded view—tanpa menggambar ulang antar-shot."
)
draw.multiline_text(
    (76, 1002),
    "\n".join(textwrap.wrap(rule_text, width=168)),
    font=FB,
    fill=(211, 215, 211),
    spacing=5,
)

canvas.save(OUT, quality=96)
print(OUT)
