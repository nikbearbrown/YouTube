# Converting One Video into Another Style Using Midjourney Pcodes

This guide explains the step-by-step process I use to transform a source video into a new artistic style with **Midjourney** (or compatible tools like Kling, VEO 3, Runway). The workflow extracts still frames, generates prompts, and re-assembles styled clips into a new video.

---

## Step 1. Extract Frames from Your Source Video

Use the `sample_videos.py` script below to sample frames from your video. By default, the script saves every 111th frame as a PNG.

```python
#!/usr/bin/env python3
import os
import cv2
import re

# Constants
SAMPLE_RATE = 111  # Save every 111th frame

def clean_filename(filename):
    """
    Clean a filename by:
    - Replacing spaces with underscores
    - Removing non-alphanumeric characters (except _ and .)
    - Collapsing consecutive underscores
    """
    cleaned = re.sub(r'\s+', '_', filename)
    cleaned = re.sub(r'[^\w\.]', '', cleaned)
    cleaned = re.sub(r'_{2,}', '_', cleaned)
    return cleaned

def sample_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    video_name = clean_filename(os.path.splitext(os.path.basename(video_path))[0])
    frame_count, saved_count = 0, 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % SAMPLE_RATE == 0:
            output_filename = f"{video_name}_frame_{frame_count:06}.png"
            cv2.imwrite(output_filename, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Saved {saved_count} frames from {video_path}")

def process_videos_in_directory(directory):
    for file in os.listdir(directory):
        if file.lower().endswith(".mp4"):
            video_path = os.path.join(directory, file)
            print(f"Processing video: {video_path}")
            sample_frames(video_path)

if __name__ == "__main__":
    current_directory = os.getcwd()
    print(f"Current directory: {current_directory}")
    process_videos_in_directory(current_directory)
```

Run the script in the same directory as your `.mp4` files:

```bash
python3 sample_videos.py
```

This will generate frames like:

```
video_name_frame_000000.png
video_name_frame_000111.png
video_name_frame_000222.png
```

---

## Step 2. Host Frames Online

Midjourney requires publicly accessible image URLs.
You can upload frames to **GitHub** (or another host). For GitHub, the raw URL format looks like this:

```
https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path>/<file.png>
```

**Example root path:**

```
https://raw.githubusercontent.com/nikbearbrown/YouTube/refs/heads/main/Art/Fuzzy_Wuzzy/
```

---

## Step 3. Generate Midjourney Prompts

Upload 10 frames at a time to ChatGPT, Claude, or similar assistants with this instruction:

```
Generate prompts for each uploaded image in the format: 
[content description], {style} --ar {aspect} --p {pcode} --ow {weight} --oref {url}[filename.png]
```

Example generated prompt:

```
A stylish woman with a vivid blue afro and henna-decorated arms rests her chin on her hand in a cluttered retro kitchen, wearing a yellow dress and jeweled choker, {style} --ar 16:9 --p abcd1234 --ow 77 --oref https://raw.githubusercontent.com/.../Beautiful_Marge_Official_Music_Video_frame_003663.png
```

---

## Step 4. Generate Stills in Target Style

Take the prompts and feed them into **Midjourney** with your desired **pcode**. This re-styles each extracted still frame.

You can repeat this process across tools such as:

* Midjourney
* Kling AI
* VEO 3
* Runway Gen-3

---

## Step 5. Re-Assemble Styled Frames into Video

Once you have styled frames, recompile them into a video using `ffmpeg`:

```bash
ffmpeg -framerate 24 -i frame_%06d.png -c:v libx264 -pix_fmt yuv420p styled_video.mp4
```

Adjust `-framerate` depending on your target look.

---

## Workflow Diagram (Mermaid)

```mermaid
flowchart LR
    A[Source Video] --> B[Extract frames with sample_videos.py<br/>(every 111th frame)]
    B --> C[Frames (.png)]
    C --> D[Host frames online<br/>(GitHub raw URLs)]
    D --> E[Generate prompt lines<br/>"[desc], {style} --ar {aspect} --p {pcode} --ow {weight} --oref {url}[file.png]"]
    E --> F{Renderer}
    F -->|Midjourney| G[Styled Stills]
    F -->|Kling / VEO 3 / Runway| H[Styled Clips]
    G --> I[Reassemble with ffmpeg<br/>(image sequence → video)]
    H --> J[Concatenate / Edit in NLE]
    I --> K[Final Styled Video]
    J --> K
```

---

## Links

* **Nik Bear Brown**
* [@nikbearbrown](https://github.com/nikbearbrown)
* [NikBearBrown.com](https://www.nikbearbrown.com/)
* [https://spotify.nikbearbrown.com](https://spotify.nikbearbrown.com)
* [https://muzak.nikbearbrown.com](https://muzak.nikbearbrown.com)
* [https://github.nikbearbrown.com](https://github.nikbearbrown.com)
* [https://youtube.nikbearbrown.com](https://youtube.nikbearbrown.com)

---
