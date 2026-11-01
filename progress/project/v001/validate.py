"""Decode the actual MP4, inspect all frames, and extract version-specific review images."""
from pathlib import Path
import argparse,json,subprocess,hashlib,re
from PIL import Image,ImageDraw

parser=argparse.ArgumentParser()
parser.add_argument('--video',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--silent',action='store_true')
args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=False)
def save(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames,sample_rate,channels','-of','json',str(args.video)],text=True))
save('media.json',meta)
vs=next(s for s in meta['streams'] if s['codec_type']=='video')
assert vs['r_frame_rate']=='30/1' and int(vs['nb_read_frames'])==384
assert abs(float(meta['format']['duration'])-12.8)<.001
KEYS=[15,60,78,120,156,180,222,252,282,305,306,307,308,310,321,366,383]
SHEETS={'overview.jpg':[15,60,78,120,156,180,222,252,282,305,308,321],
        'transitions.jpg':[75,81,87,90,93,96,102,108,162,168,174,180,246,252,258,264],
        'impact.jpg':list(range(300,320))}
selected=set(KEYS)
for frames in SHEETS.values():selected.update(frames)
thumbs={};rows=[];flash=[]
cmd=['ffmpeg','-v','error','-nostdin','-xerror','-i',str(args.video),'-an','-vf','scale=480:270','-pix_fmt','rgb24','-f','rawvideo','-']
proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
frame=0;frame_size=480*270*3
while True:
 raw=b''
 while len(raw)<frame_size:
  chunk=proc.stdout.read(frame_size-len(raw))
  if not chunk:break
  raw+=chunk
 if not raw:break
 assert len(raw)==frame_size
 im=Image.frombytes('RGB',(480,270),raw)
 histogram=im.convert('L').histogram();visible=sum(histogram[70:])
 mask=im.convert('L').point(lambda v:255 if v>70 else 0);box=mask.getbbox()
 r,g,b=im.getpixel((20,20))
 if r>80 and r>g*2:flash.append(frame)
 rows.append({'frame':frame,'foreground_pixels':visible,'foreground_bbox':box})
 if frame in selected:thumbs[frame]=im.copy()
 frame+=1
error=proc.stderr.read().decode();code=proc.wait();assert code==0,error
assert frame==384
assert all(row['foreground_pixels']>10 for row in rows),'Visually empty frame detected'
assert flash==[306,307],flash
edge=[r['frame'] for r in rows if r['frame'] not in flash and r['foreground_bbox'] and (r['foreground_bbox'][0]<=0 or r['foreground_bbox'][1]<=0 or r['foreground_bbox'][2]>=480 or r['foreground_bbox'][3]>=270)]
save('frame-audit.json',{'method':'480x270 decoded luma >70 foreground mask; border pixel red-flash check; not semantic visual judgment','frames':rows,'red_flash_frames':flash,'foreground_touches_edge':edge,'decode_exit_code':code,'stderr':error})
for name,frames in SHEETS.items():
 columns=5 if name=='impact.jpg' else 4
 sheet=Image.new('RGB',(columns*480,((len(frames)+columns-1)//columns)*298),'#252528');draw=ImageDraw.Draw(sheet)
 for i,f in enumerate(frames):
  x=i%columns*480;y=i//columns*298;sheet.paste(thumbs[f],(x,y));draw.text((x+8,y+276),f'{f:03d} | {f/30:.3f}s',fill='white')
 sheet.save(out/name,quality=95)
(out/'keyframes').mkdir()
for f in KEYS:
 subprocess.run(['ffmpeg','-v','error','-nostdin','-ss',f'{f/30:.9f}','-i',str(args.video),'-frames:v','1','-threads','1',str(out/'keyframes'/f'frame-{f:06d}.png')],check=True)
save('samples.json',{'source_sha256':hashlib.sha256(args.video.read_bytes()).hexdigest(),'fps':30,'frame_number_origin':0,'keyframes':[{'path':f'keyframes/frame-{f:06d}.png','frame':f,'time_seconds':f/30} for f in KEYS],'sheets':SHEETS})
audio={'status':'not_present_in_silent_draft'}
if not args.silent:
 stream=next(s for s in meta['streams'] if s['codec_type']=='audio')
 assert stream['codec_name']=='aac' and stream['sample_rate']=='48000' and stream['channels']==2
 result=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-xerror','-i',str(args.video),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True)
 (out/'decode-loudness.log').write_text('\n'.join(line.rstrip() for line in result.stderr.splitlines())+'\n')
 summary=result.stderr.rsplit('Summary:',1)[-1]
 integrated=float(re.search(r'I:\s*([-\d.]+) LUFS',summary).group(1));peak=float(re.search(r'Peak:\s*([-\d.]+) dBFS',summary).group(1))
 assert -14.5<=integrated<=-13.5 and peak<=-1
 audio={'status':'measured','integrated_lufs':integrated,'true_peak_dbtp':peak,'word_level_alignment':'not_verified'}
save('summary.json',{'decoded_frames':frame,'no_empty_frames':True,'red_flash_frames':flash,'foreground_touches_edge':edge,'audio':audio,'limits':'Image sampling and signal checks do not establish exact sung word timing or artistic approval.'})
print(json.dumps({'frames':frame,'flash_frames':flash,'edge_frames':edge,'audio':audio},ensure_ascii=False))
