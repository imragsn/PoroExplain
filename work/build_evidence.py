from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent
ANALYSIS=ROOT/'video-analysis'
OUTPUT=ROOT.parent/'outputs'
FONTS='C:/Windows/Fonts/'
FONT=ImageFont.truetype(FONTS+'arialbd.ttf',20)
SMALL=ImageFont.truetype(FONTS+'arial.ttf',17)
TITLES={'A':'MOTOR LISTRIK ATAU BENSIN','B':'ISI BENSIN','C':'CARA KERJA MOTOR MATIC'}

def get_frame(key,time,label):
    target=ANALYSIS/key/f'{label}.png'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',f'C:/Users/lenovo/Downloads/{TITLES[key]}.mp4','-frames:v','1',str(target)],check=True)
    return target

evidence=[('A',0.5,'harga'),('A',45.5,'baterai'),('A',60.5,'grafik'),('B',0.5,'pompa'),('B',20.5,'potongan'),('B',68.5,'keputusan'),('C',0.5,'mekanisme'),('C',20.5,'roller'),('C',30.5,'belt')]
boundaries=[('A',0,'start'),('A',76.3,'end'),('B',0,'start'),('B',78.33,'end'),('C',0,'start'),('C',42.1,'end')]
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(lambda p:get_frame(*p),evidence+boundaries))

sheet=Image.new('RGB',(900,3*579+60),'#f0f0ec')
d=ImageDraw.Draw(sheet)
d.text((18,19),'BUKTI VISUAL | tiga referensi | timestamp sampel',font=FONT,fill='#151515')
for n,(key,t,label) in enumerate(evidence):
    x=(n%3)*300;y=60+(n//3)*579
    im=Image.open(ANALYSIS/key/f'{label}.png').convert('RGB').resize((300,533))
    sheet.paste(im,(x,y))
    d.text((x+9,y+540),f'{key} {t:04.1f}s | {label}',font=SMALL,fill='#151515')
sheet.save(OUTPUT/'papan-bukti-visual.jpg',quality=94)

loop=Image.new('RGB',(900,3*579+60),'#f0f0ec')
d=ImageDraw.Draw(loop)
d.text((18,19),'SAMBUNGAN VISUAL | akhir -> awal (gambar diam)',font=FONT,fill='#151515')
for row,key in enumerate(['A','B','C']):
    end=Image.open(ANALYSIS/key/'end.png').convert('RGB').resize((300,533))
    start=Image.open(ANALYSIS/key/'start.png').convert('RGB').resize((300,533))
    loop.paste(end,(0,60+row*579))
    loop.paste(start,(300,60+row*579))
    d.text((615,100+row*579),key,font=FONT,fill='black')
    d.text((615,140+row*579),'Kiri: akhir',font=SMALL,fill='black')
    d.text((615,170+row*579),'Tengah: awal',font=SMALL,fill='black')
    d.text((10,60+row*579+540),TITLES[key],font=SMALL,fill='black')
loop.save(ANALYSIS/'loop-boundaries.jpg',quality=94)

palette={}
for key,label in [('A','harga'),('B','pompa'),('C','mekanisme')]:
    im=Image.open(ANALYSIS/key/f'{label}.png').convert('RGB')
    w,h=im.size
    crop=im.crop((int(w*.60),int(h*.02),int(w*.90),int(h*.06)))
    color=crop.resize((1,1)).getpixel((0,0))
    palette[key]={'background_sample_rgb':color,'background_sample_hex':'#'+''.join(f'{v:02x}' for v in color),'sample_area':'x=60-90%, y=2-6% on frame t=0.5s; decoded PNG'}
(ANALYSIS/'palette-samples.json').write_text(json.dumps(palette,indent=2),encoding='utf-8')
print(json.dumps(palette,indent=2))
