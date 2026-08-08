import cv2
import numpy as np
from tqdm import tqdm
from OsuBuilder import OsuBuilder

def ar_to_ms(ar: float, od:  float):
    if   ar < 5 : t = 1200 + 120 * (5 - ar)
    elif ar == 5: t = 1200 
    else:         t = 1200 - 150 * (ar - 5)
    
    w50 = 200 - 10 * od
    
    return t + w50

def cs_to_scale(cs):
    r = (54.4 - (4.48 * cs)) 
    return r

class OsuAsMp4Player:
    def __init__(self) -> None:
        self.get_stats()

    def get_stats(self): 
        for cs in range(0, 12, 1):
            r = cs_to_scale(cs)
            print(cs, r)

        for od in range(0, 12):
            for ar in range(0, 12):
                for hd in [True, False]:
                    ms = self.arod_to_ms(ar, od, use_hd=hd)
                    fps = 1000 / ms
                    print(f'AR: {ar:2d}, OD: {od:2d}, HD: {str(hd):<5} | Doba noty: {ms:6.1f} ms -> {fps:.2f}fps')

    @staticmethod
    def cs_to_scale(cs: float):
        r = (54.4 - (4.48 * cs)) 
        return r

    @staticmethod
    def arod_to_ms(ar: float, od:float, use_hd: bool = False):
        if   ar < 5 : t = 1200 + 120 * (5 - ar)
        elif ar == 5: t = 1200 
        else:         t = 1200 - 150 * (ar - 5)
        
        if use_hd: 
            return t * 0.7

        w50 = 200 - 10 * od
        
        return t + w50

if __name__ == "__main__":
    app = OsuAsMp4Player()

'''
video_path = "bad_apple.mp4"
cap = cv2.VideoCapture(video_path)

start_sec = 0
end_sec = 60.0
target_fps = 5
target_size = (w, h)

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

with tqdm(total=expected_frames, desc="Process video", unit="frame") as pbar:
    while current_native_frame < end_frame:
        ret, frame = cap.read()
        if not ret:
            break

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

output_filename = "vystup.mp4"
fps = target_fps
height, width = target_size[1], target_size[0]

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

map = OsuBuilder(title="Test", version="Hard", cs=CS)

d, h, w = video_matrix.shape

offset = 0
for frame in video_matrix:
    offset += 1000

    for y in range(0, h):
        for x in range(0, w):
            if frame[y][x] == 0:
                map.add_circle(cr + (cd * x), cr + (cd * y), offset)

    frame_255 = (frame * 255).astype(np.uint8)

    frame_bgr = cv2.cvtColor(frame_255, cv2.COLOR_GRAY2BGR)

    out.write(frame_bgr)

map.save('output')

out.release()
'''



