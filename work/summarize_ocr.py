from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent/'video-analysis'
for key in ['A','B','C']:
    data=json.loads((ROOT/key/'ocr.json').read_text(encoding='utf-8-sig'))
    rows=[]
    for entry in data:
        title=[]
        captions=[]
        for line in entry['lines']:
            words=line['words']
            if not words: continue
            y=min(w['y'] for w in words)
            if 45 <= y < 105:
                title.append(line['text'])
            if (370 if key=='C' else 405) <= y < 495:
                captions.append(line['text'])
        rows.append(f"{entry['approx_seconds']:05.1f}s | {' / '.join(title)} | {' / '.join(captions)}")
    (ROOT/key/'ocr-summary.txt').write_text('\n'.join(rows),encoding='utf-8')
    print(key+'\n'+'\n'.join(rows))
