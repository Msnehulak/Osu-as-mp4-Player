import os
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent

class OsuBuilder:
    def __init__(self, title="Song", artist="Artist", creator="Bot", version="Normal"):
        self.metadata = {
            'title': title,
            'artist': artist,
            'creator': creator,
            'version': version
        }
        self.metadata_f = f"[Metadata]\nTitle:{title}\nArtist:{artist}\nCreator:{creator}\nVersion:{version}\n"
        self.circles = []

    def add_circle(self, x: int, y: int, time_ms: int):
        # x, y, time, type=1 (Circle), hitSound=0
        self.circles.append(f"{x},{y},{time_ms},1,0,0:0:0:0:")

    def save(self, filepath: str):
        content = [
            "osu file format v14\n",
            "[General]\nAudioFilename: audio.mp3\nMode: 0\n",
            self.metadata_f,
            "[Difficulty]\nHPDrainRate:5\nCircleSize:4\nOverallDifficulty:5\nApproachRate:8\nSliderMultiplier:1.4\nSliderTickRate:1\n",
            "[TimingPoints]\n0,500,4,1,0,100,1,0\n",  # Základní timing (120 BPM)
            "[HitObjects]"
        ] + self.circles
        
        temp_f = BASE_DIR / 'temp' 
        temp_f.mkdir(parents=True, exist_ok=True)

        filepath = BASE_DIR / f'{filepath}'
            
        i = self.metadata
        name = f'{i['artist']} - {i['title']} ({i['creator']}) [{i['version']}].osu'

        path = temp_f / name
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        temp_f = BASE_DIR / 'temp' 
        shutil.make_archive(filepath, 'zip',  temp_f)
       
        os.rename(f"{filepath}.zip", f"{filepath}.osz")
        shutil.rmtree(temp_f)

if __name__ == '__main__':
    builder = OsuBuilder(title="Test", version="Hard")
    builder.add_circle(256, 192, 1000)
    builder.add_circle(100, 100, 2000)
    builder.save("output1")
            



