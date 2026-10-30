from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'video-analysis'
OUT.mkdir(exist_ok=True)
VIDEOS = [
    ('A', 'MOTOR LISTRIK ATAU BENSIN'),
    ('B', 'ISI BENSIN'),
    ('C', 'CARA KERJA MOTOR MATIC'),
]
FONT = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
SMALL = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 17)

def run(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)

def process(item):
    key, title = item
    source = Path('C:/Users/lenovo/Downloads') / (title + '.mp4')
    folder = OUT / key
    folder.mkdir(exist_ok=True)
    meta = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(source)]).stdout)
    (folder / 'metadata.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source), '-vf', 'fps=1,scale=360:640', '-q:v', '3', str(folder / 'frame-%03d.jpg')])
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source), '-vn', '-ar', '16000', '-ac', '1', str(folder / 'audio.wav')])
    duration = float(meta['format']['duration'])
    video = next(s for s in meta['streams'] if s['codec_type'] == 'video')
    frames = sorted(folder.glob('frame-*.jpg'))
    # fps=1 output samples are centered near t=n+0.5; exact frame times are
    # established separately for any close timing analysis.
    selected = list(range(0, len(frames), 5))
    if len(frames)-1 not in selected:
        selected.append(len(frames)-1)
    cols, tw, th = 4, 270, 480
    rows = (len(selected)+cols-1)//cols
    sheet = Image.new('RGB', (cols*tw, 54+rows*(th+29)), '#e9e9e9')
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 15), f'{key} | {title} | {duration:.3f}s', font=FONT, fill='#111111')
    for n, idx in enumerate(selected):
        x, y = (n%cols)*tw, 54+(n//cols)*(th+29)
        im = Image.open(frames[idx]).resize((tw,th))
        sheet.paste(im,(x,y))
        draw.text((x+6,y+th+4),f'~{idx+0.5:05.1f}s',font=SMALL,fill='#111111')
    sheet.save(folder/'overview.jpg',quality=92)
    return {'id':key,'title':title,'duration':duration,'width':video['width'],'height':video['height'],'fps':video['avg_frame_rate'],'frames':len(frames),'overview':str(folder/'overview.jpg')}

with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(process, VIDEOS))
(OUT/'inventory.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
