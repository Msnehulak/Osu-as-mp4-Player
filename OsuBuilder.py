import os
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / 'temp'

class OsuBuilder:
    def __init__(self, title="Song", artist="Artist", creator="Bot", version="Normal",
            cs=5, hp=5, od=5, ar=8 
        ):
        self.metadata = {
            'title': title,
            'artist': artist,
            'creator': creator,
            'version': version
        }
        self.diff = {
            'cs': cs,  'hp': hp,
            'od': od,  'ar': ar
        }
        self.circles = []
        self._update_map_data()

    def _update_map_data(self):
        md = self.metadata
        self.map_name = f'{md['artist']} - {md['title']} ({md['creator']}) [{md['version']}].osu'
        metadata = [
            f"[Metadata]",
            f"Title:{md['title']}",
            f"Artist:{md['artist']}",
            f"Creator:{md['creator']}",
            f"Version:{md['version']}",
        ]

        dd = self.diff
        diff = [
            "[Difficulty]",
            f"HPDrainRate:{dd['hp']}",
            f"CircleSize:{dd['cs']}",
            f"OverallDifficulty:{dd['od']}",
            f"ApproachRate:{dd['ar']}",
            f"SliderMultiplier:1.4",
            f"SliderTickRate:1"
        ]

        self.content = [
            "osu file format v14\n",
            "[General]\nAudioFilename: audio.mp3\nMode: 0\n",
            f"{'\n'.join(metadata)}",
            f"{'\n'.join(diff)}",
            "[TimingPoints]\n0,500,4,1,0,100,1,0\n",  # Základní timing (120 BPM)
            "[HitObjects]"
        ] + self.circles

    def add_circle(self, x: int, y: int, time_ms: int):
        self.circles.append(f"{x},{y},{time_ms},1,0,0:0:0:0:")

    def _create_temp_file(self):
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(TEMP_DIR)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

    def save(self, name: str):
        self._update_map_data()
        self._create_temp_file()

        filepath = BASE_DIR / name
            
        path = TEMP_DIR / self.map_name
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.content))

        shutil.make_archive(f'{filepath}', 'zip',  TEMP_DIR)
       
        os.rename(f"{filepath}.zip", f"{filepath}.osz")
        shutil.rmtree(TEMP_DIR)

if __name__ == '__main__':
    builder = OsuBuilder(title="Test", version="Hard", cs=10)
    offset = 0
    for i in range(0, 512, 16):
        for x in range(0, 384, 16):
            offset += 1
            builder.add_circle(i+8, x+8, 1000+offset)

    builder.save('bad_apple')
            



