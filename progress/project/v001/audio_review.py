"""Plot audio energy against planned cues; this is not speech recognition or word alignment."""
from pathlib import Path
from array import array
import argparse,json,math,subprocess
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
PROGRESS=next(p for p in ROOT.parents if (p/'catalog.json').is_file())
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
args.output.mkdir(parents=True,exist_ok=False)
cfg=json.loads((ROOT/'timeline.json').read_text())
raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(cfg['audio_in']),'-i',str(PROGRESS/cfg['audio_source']),'-t',str(cfg['audio_duration']),'-vn','-ar','16000','-ac','1','-f','s16le','-'])
values=array('h');values.frombytes(raw)
rows=[]
for start in range(0,len(values),320):
 chunk=values[start:start+320]
 rms=math.sqrt(sum(v*v for v in chunk)/len(chunk))/32768
 diff=math.sqrt(sum((chunk[i]-chunk[i-1])**2 for i in range(1,len(chunk)))/max(1,len(chunk)-1))/32768
 rows.append({'time':start/16000,'rms':rms,'high_frequency_difference_rms':diff})
data={'method':'20ms mono RMS and sample-difference RMS; includes instruments, so not word-level alignment','cues':cfg,'envelope':rows}
(args.output/'envelope.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
im=Image.new('RGB',(1920,540),'#17181b');d=ImageDraw.Draw(im)
for sec in range(14):
 x=70+sec/12.8*1800;d.line((x,60,x,450),fill='#36383d');d.text((x+3,462),str(sec)+'s',fill='white')
maximum=max(row['rms'] for row in rows)
for row in rows:
 x=70+row['time']/12.8*1800;h=row['rms']/maximum*300
 d.line((x,420-h,x,420),fill='#e6d8c6',width=2)
for label,time in [('second',cfg['second']['start']),('Rise',cfg['third']['start']),('see',cfg['fourth']['see']),('flash',cfg['fifth']['flash']),('kill lands',cfg['fifth']['landing'])]:
 x=70+time/12.8*1800;d.line((x,40,x,440),fill='#e5364f',width=2);d.text((x-20,20 if label!='kill lands' else 45),label,fill='#ff8996')
d.text((70,500),'Waveform cues only. Sung word boundaries are not verified by this plot.',fill='white')
im.save(args.output/'waveform.png')
print('Audio cue evidence saved; no word-level alignment claimed.')
