"""Keep the original song excerpt, master it in two passes, and mux a rendered video."""
from pathlib import Path
import argparse, json, re, subprocess

ROOT=Path(__file__).resolve().parent
PROGRESS=next(p for p in ROOT.parents if (p/'catalog.json').is_file())
parser=argparse.ArgumentParser()
parser.add_argument('--silent',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
cfg=json.loads((ROOT/'timeline.json').read_text())
out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
if (out/'video.mp4').exists():raise FileExistsError(out/'video.mp4')
production=out/'production';production.mkdir(exist_ok=True)
audio=PROGRESS/'assets/audio/five-lines-17.6-29.3.wav';audio.parent.mkdir(exist_ok=True)
if not audio.exists():
 subprocess.run(['ffmpeg','-v','error','-nostdin','-ss',str(cfg['audio_in']),'-i',str(PROGRESS/cfg['audio_source']),'-t',str(cfg['audio_duration']),'-vn','-ar','48000','-ac','2','-c:a','pcm_s24le',str(audio)],check=True)
common='afade=t=in:d=0.02,afade=t=out:st=11.35:d=0.35,apad=whole_dur=12.8,'
first=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(audio),'-af',common+'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
(production/'loudness-pass1.log').write_text('\n'.join(line.rstrip() for line in first.stderr.splitlines())+'\n')
measure=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',first.stderr).group())
(production/'loudness-pass1.json').write_text(json.dumps(measure,indent=2)+'\n')
filters=common+'loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true'.format(**measure)
cmd=['ffmpeg','-v','warning','-nostdin','-i',str(args.silent),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',filters,'-c:a','aac','-b:a','320k','-ar','48000','-ac','2','-t',str(cfg['duration']),'-movflags','+faststart',str(out/'video.mp4')]
subprocess.run(cmd,check=True)
(production/'mux.json').write_text(json.dumps({'command':cmd,'audio_source':'assets/audio/five-lines-17.6-29.3.wav','filters':filters,'duration':cfg['duration']},ensure_ascii=False,indent=2)+'\n')
print('Original song excerpt mastered and muxed:',out/'video.mp4')
