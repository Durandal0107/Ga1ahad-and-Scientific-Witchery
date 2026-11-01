"""Deterministic SVG rendering with system Chromium. Run --help for output modes."""
from pathlib import Path
import argparse, base64, json, subprocess
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
PROGRESS=next(p for p in ROOT.parents if (p/'catalog.json').is_file())
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--width',type=int,default=1920)
parser.add_argument('--stills',action='store_true')
args=parser.parse_args()
timeline=json.loads((ROOT/'timeline.json').read_text())
html=(ROOT/'index.html').read_text()
for script in ('lettering.js','scene.js'):
 html=html.replace(f'<script src="{script}"></script>','<script>'+ (ROOT/script).read_text()+'</script>')
font=PROGRESS/'assets/fonts/Z003-MediumItalic.otf'
html=html.replace('../../assets/fonts/Z003-MediumItalic.otf','data:font/otf;base64,'+base64.b64encode(font.read_bytes()).decode())
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--font-render-hinting=none'])
 page=browser.new_page(viewport={'width':args.width,'height':args.width*9//16},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda error: errors.append(str(error)))
 page.set_content(html);page.evaluate("document.fonts.load('100px Chancery')")
 page.evaluate('(c)=>window.C=c',timeline)
 if args.stills:
  args.output.mkdir(parents=True,exist_ok=False)
  for frame in (15,60,78,120,156,180,222,252,282,305,309,321,366):
   page.evaluate('(t)=>render(t)',frame/timeline['fps'])
   page.screenshot(path=str(args.output/f'frame-{frame:06d}.png'))
  print('Rendered 13 design stills',flush=True)
 else:
  args.output.parent.mkdir(parents=True,exist_ok=True)
  if args.output.exists():raise FileExistsError(args.output)
  cmd=['ffmpeg','-v','warning','-nostdin','-f','image2pipe','-vcodec','png','-framerate',str(timeline['fps']),'-i','-','-an','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-threads','3','-movflags','+faststart',str(args.output)]
  encoder=subprocess.Popen(cmd,stdin=subprocess.PIPE)
  try:
   for frame in range(round(timeline['duration']*timeline['fps'])):
    page.evaluate('(t)=>render(t)',frame/timeline['fps'])
    encoder.stdin.write(page.screenshot(type='png'))
    if frame%60==0:print(f'{frame}/384',flush=True)
  finally:
   encoder.stdin.close()
  if encoder.wait():raise RuntimeError('FFmpeg encoding failed')
 if errors:raise RuntimeError(errors)
 browser.close()
