from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'outputs'
WORK=ROOT/'work'/'termos-audio'
audio=OUT/'termos-04-narasi-v0.1.mp3'
script=OUT/'termos-04-narasi-v0.1.txt'
probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(audio)],capture_output=True,text=True,check=True).stdout)
duration=float(probe['format']['duration'])
stream=next(s for s in probe['streams'] if s['codec_type']=='audio')

def parse_time(value):
    hh,mm,rest=value.split(':')
    ss,millis=rest.split(',')
    return int(hh)*3600+int(mm)*60+int(ss)+int(millis)/1000

def timecode(value):
    total=round(value*1000)
    hh,rest=divmod(total,3600000)
    mm,rest=divmod(rest,60000)
    ss,millis=divmod(rest,1000)
    return f'{hh:02}:{mm:02}:{ss:02},{millis:03}'

raw= (WORK/'take-v1.srt').read_text(encoding='utf-8-sig')
matches=re.findall(r'\d+\s*\n(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)\s*\n(.*?)(?=\n\s*\n|\Z)',raw,flags=re.S)
mapping=[
    ('B01','momen sehari-hari',['P-02'],[],'Termos dibuka dan minuman dituangkan; bunyi dibuat pada tahap rakit.'),
    ('B02','pertanyaan utama',[],[],'Pertahankan benda sebagai fokus dan tampilkan pertanyaan.'),
    ('B03','membuka penjelasan',['P-03','P-05','P-06'],[],'Beralih dari benda utuh ke penampang yang sudah diterima.'),
    ('B04','identifikasi dinding',['P-03','P-06'],['F-01'],'Sorot dua dinding; cue label per kata disusun setelah audio diterima.'),
    ('B05','mengenalkan vakum',['P-05'],['F-01'],'Sorot celah di antara dinding; tunjukkan lokasi yang benar.'),
    ('B06','fungsi celah',['P-05'],['F-01'],'Ilustrasikan penghambatan transfer melalui gas tanpa memberi nilai watt atau tekanan.'),
    ('B07','jalur radiasi',['P-04'],['F-01'],'Tunjukkan bahwa jalur radiasi masih dapat melintasi celah; arah energi konseptual.'),
    ('B08','lapisan reflektif',['P-04'],['F-02'],'Sorot permukaan di sisi luar dinding dalam; warna hanya penanda ilustratif.'),
    ('B09','fungsi tutup',['P-01'],['F-03'],'Sorot penutup dan area seal; jangan menambahkan komponen yang belum didukung sumber.'),
    ('B10','jalur tersisa',['P-03','P-06'],['F-04'],'Tunjukkan sambungan leher sebagai salah satu jalur yang masih tersisa.'),
    ('B11','jawaban mekanisme',['P-01','P-03','P-04','P-05','P-06'],['F-01','F-02','F-03','F-04'],'Rangkum penghambatan jalur panas; tidak menampilkan kurva pendinginan rekaan.'),
    ('B12','contoh spesifikasi',[],['F-05'],'Kartu menyebut SM-WA48, suhu awal beserta toleransi, durasi, batas akhir, dan kondisi ruangan; data diambil dari JSON riset.'),
    ('B13','jembatan loop',[],[],'Kembali ke keadaan menjelang pembukaan; sambungkan ke awal tanpa menambah fakta baru.'),
]
assert len(matches)==len(mapping), (len(matches),len(mapping))
cues=[]
for (start,end,text),(key,function,parts,claims,action) in zip(matches,mapping):
    cues.append({'id':key,'start_seconds':round(max(0,parse_time(start)-0.17),3),'end_seconds':round(min(duration,parse_time(end)-0.17),3),'text':' '.join(text.split()),'function':function,'part_ids':parts,'claim_ids':claims,'planned_visual':action,'word_alignment_status':'pending_user_audio_feedback'})
for i,cue in enumerate(cues[:-1]):
    cue['end_seconds']=min(cue['end_seconds'],cues[i+1]['start_seconds'])
for cue in cues:
    assert 0<=cue['start_seconds']<cue['end_seconds']<=duration
caption_text=' '.join(c['text'] for c in cues)
script_text=script.read_text(encoding='utf-8')
assert ' '.join(script_text.split())==caption_text

subtitle='\n\n'.join(f"{i+1}\n{timecode(c['start_seconds'])} --> {timecode(c['end_seconds'])}\n{c['text']}" for i,c in enumerate(cues))+'\n'
(OUT/'termos-04-cue-kalimat-v0.1.srt').write_text(subtitle,encoding='utf-8')

manifest={
    'status':'awaiting_user_audio_feedback',
    'audio_file':audio.name,
    'script_file':script.name,
    'sentence_cues_file':'termos-04-cue-kalimat-v0.1.srt',
    'duration_seconds':duration,
    'word_count_whitespace':len(script_text.split()),
    'voice':{'provider':'Microsoft Edge Read Aloud through edge-tts','id':'id-ID-ArdiNeural','locale':'id-ID','rate':'+0%','single_full_text_synthesis':True},
    'external_text_permission':{'status':'explicitly_approved','user_reply':'Boleh, buat audionya','destination_host':'speech.platform.bing.com','payload':'termos narration v0.1 text'},
    'edits':{'source_duration_seconds':52.68,'source_in_seconds':0.17,'source_out_seconds':51.93,'internal_speech_splices':False,'purpose':'trim leading and trailing silence only'},
    'format':{'codec':stream['codec_name'],'sample_rate_hz':int(stream['sample_rate']),'channels':stream['channels']},
    'verification':{'decode_succeeded':True,'provider_caption_text_matches_input':True,'local_asr_completed':True,'asr_brand_spelling':'Zodirushi','asr_spelling_is_not_a_pronunciation_verdict':True,'perceptual_listening_by_assistant':False,'word_level_alignment_completed':False},
    'hashes':{'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'audio_sha256':hashlib.sha256(audio.read_bytes()).hexdigest()},
    'cues':cues,
}
(OUT/'termos-04-cue-v0.1.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
rows=['| Waktu acuan | Kalimat | Fungsi | Arah visual |','|---|---|---|---|']
for cue in cues:
    rows.append(f"| {cue['start_seconds']:.2f}–{cue['end_seconds']:.2f} dtk | {cue['text']} | {cue['function']} | {cue['planned_visual']} |")
(WORK/'cue-table.md').write_text('\n'.join(rows),encoding='utf-8')
print(json.dumps({'duration_seconds':duration,'sentence_cues':len(cues),'script_matches_captions':True,'word_count':manifest['word_count_whitespace']},ensure_ascii=False))
