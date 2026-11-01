"""Extract a reproducible visual review of the uploaded 384-frame, 30 fps clip.

Run from any directory: python3 progress/tools/review_uploaded_video.py OUTPUT_DIR
OUTPUT_DIR must not exist. Requires ffmpeg, ffprobe and Pillow. Never edits the video.
"""

import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "versions/legacy-upload-001/video.mp4"
OVERVIEW = [0, 15, 38, 75, 90, 120, 160, 170, 183, 195, 210, 240, 255, 270, 288, 306, 312, 321, 345, 381]
KEYFRAMES = [38, 75, 120, 160, 183, 195, 240, 255, 288, 306, 312, 321, 360]
TRANSITIONS = list(range(165, 196, 3)) + list(range(249, 277, 3))
IMPACT = list(range(303, 328))


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main(output):
    output.mkdir(parents=True, exist_ok=False)
    (output / "keyframes").mkdir()
    metadata = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-count_frames", "-show_entries",
        "format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,nb_read_frames,sample_rate,channels",
        "-of", "json", str(SOURCE)], text=True))
    stream = next(s for s in metadata["streams"] if s["codec_type"] == "video")
    assert stream["r_frame_rate"] == "30/1" and int(stream["nb_read_frames"]) == 384
    dump(output / "media.json", metadata)
    samples = sorted(set(OVERVIEW + KEYFRAMES + TRANSITIONS + IMPACT))
    thumbs = {}
    for frame in samples:
        png = subprocess.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{frame / 30:.9f}", "-i", str(SOURCE),
            "-frames:v", "1", "-f", "image2pipe", "-c:v", "png", "-threads", "1", "-"])
        if frame in KEYFRAMES:
            (output / "keyframes" / f"frame-{frame:06d}.png").write_bytes(png)
        with Image.open(io.BytesIO(png)) as image:
            thumbs[frame] = image.convert("RGB").resize((480, 270))
    sheets = {"overview.jpg": OVERVIEW, "transitions.jpg": TRANSITIONS, "impact.jpg": IMPACT}
    for name, frames in sheets.items():
        columns = 4 if name != "impact.jpg" else 5
        sheet = Image.new("RGB", (columns * 480, ((len(frames) + columns - 1) // columns) * 298), "#222222")
        draw = ImageDraw.Draw(sheet)
        for i, frame in enumerate(frames):
            x, y = (i % columns) * 480, (i // columns) * 298
            sheet.paste(thumbs[frame], (x, y))
            draw.text((x + 8, y + 276), f"frame {frame:03d} | {frame / 30:.3f}s", fill="white")
        sheet.save(output / name, quality=95)
    dump(output / "samples.json", {
        "source": "../video.mp4", "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "fps": 30, "frame_number_origin": 0,
        "keyframes": [{"path": f"keyframes/frame-{f:06d}.png", "frame": f, "time_seconds": f / 30} for f in KEYFRAMES],
        "sheets": {name: [{"frame": f, "time_seconds": f / 30} for f in frames] for name, frames in sheets.items()},
        "limits": "Visual samples and frame-by-frame impact review; no word-level audio alignment is claimed."})
    command = ["ffmpeg", "-hide_banner", "-nostdin", "-xerror", "-i", str(SOURCE), "-af", "ebur128=peak=true", "-f", "null", "-"]
    result = subprocess.run(command, capture_output=True, text=True)
    # Normalize terminal-only trailing whitespace while retaining all log lines.
    (output / "decode-loudness.log").write_text("\n".join(line.rstrip() for line in result.stderr.splitlines()) + "\n")
    dump(output / "verification.json", {"command": command, "exit_code": result.returncode,
                                         "audio_alignment": "not_performed"})
    result.check_returncode()
    print(f"Saved {len(KEYFRAMES)} keyframes, 3 contact sheets, metadata and decode/loudness evidence.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: review_uploaded_video.py OUTPUT_DIR (new directory)")
    main(Path(sys.argv[1]))
