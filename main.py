import sys
import cv2
import numpy as np
from tqdm import tqdm
from OsuBuilder import OsuBuilder

CS = 6

def cs_to_scale(cs):
    r = (54.4 - (4.48 * cs)) 
    d = r * 2
    return round(r), round(d)

cr, cd = cs_to_scale(CS)
w = 512 // cd
h = 384 // cd

video_path = "bad_apple.mp4"
cap = cv2.VideoCapture(video_path)

# --- Nastavení parametrů ---
start_sec = 0
end_sec = 60.0
target_fps = 5
target_size = (w, h)

# --- Získání vlastností ---
native_fps = cap.get(cv2.CAP_PROP_FPS)
total_native_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

start_frame = int(start_sec * native_fps)
end_frame = int(end_sec * native_fps) if end_sec else total_native_frames
end_frame = min(end_frame, total_native_frames)

step = native_fps / target_fps

cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

frames_array = []
current_native_frame = start_frame
next_target_frame = float(start_frame)

expected_frames = int((end_frame - start_frame) / step)

with tqdm(total=expected_frames, desc="Rychlé zpracování", unit="frame") as pbar:
    while current_native_frame < end_frame:
        # Plynulé čtení bez cap.set()
        ret, frame = cap.read()
        if not ret:
            break

        # Uložíme pouze snímek, který odpovídá našemu cílovému FPS
        if current_native_frame >= next_target_frame:
            resized = cv2.resize(
                frame, target_size, interpolation=cv2.INTER_AREA
            )
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            _, binary_frame = cv2.threshold(gray, 127, 1, cv2.THRESH_BINARY)

            frames_array.append(binary_frame)

            next_target_frame += step
            pbar.update(1)

        current_native_frame += 1

cap.release()

video_matrix = np.array(frames_array, dtype=np.uint8)
print("Hotovo! Rychlost je zpět. Tvar:", video_matrix.shape)


output_filename = "vystup.mp4"
fps = target_fps  # Vaše cílové FPS (např. 10)
height, width = target_size[1], target_size[0]

# 1. Definice kodeku a vytvoření VideoWriteru
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Kodek pro MP4 (případně 'avc1' nebo 'XVID')
out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

# 2. Zápis snímků
map = OsuBuilder(title="Test", version="Hard", cs=CS)

d, h, w = video_matrix.shape

offset = 0
for frame in video_matrix:
    offset += 1000

    for y in range(0, h):
        for x in range(0, w):
            if frame[y][x] == 0:
                map.add_circle(cr + (cd * x), cr + (cd * y), offset)

    # Převod z hodnot 0/1 na 0/255 (černá/bílá)
    frame_255 = (frame * 255).astype(np.uint8)

    # MP4 vyžaduje 3-kanálový obraz (BGR)
    frame_bgr = cv2.cvtColor(frame_255, cv2.COLOR_GRAY2BGR)

    out.write(frame_bgr)

map.save()

out.release()
print(f"MP4 video bylo úspěšně uloženo do {output_filename}")
