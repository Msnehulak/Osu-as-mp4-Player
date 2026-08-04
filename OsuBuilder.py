import os
from pathlib import Path
import shutil

from cv2 import DISOpticalFlow_PRESET_MEDIUM

BASE_DIR = Path(__file__).resolve().parent

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
        self._map_data_update()

    def _map_data_update(self):
        md = self.metadata
        self.name = f'{md['artist']} - {md['title']} ({md['creator']}) [{md['version']}].osu'

        metadata = [
            f"[Metadata]",
            f"Title:{md['title']}",
            f"Artist:{md['artist']}",
            f"Creator:{md['creator']}",
            f"Version:{md['version']}",
        ]
        self.smetadata = '\n'.join(metadata)

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

        self.sdiff = '\n'.join(diff)

    def add_circle(self, x: int, y: int, time_ms: int):
        self.circles.append(f"{x},{y},{time_ms},1,0,0:0:0:0:")

    def _create_temp_file(self):
        self.temp_file.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(self.temp_file)
        self.temp_file.mkdir(parents=True, exist_ok=True)
        print('>>> temp folder clear and crear')

    def save(self):
        content = [
            "osu file format v14\n",
            "[General]\nAudioFilename: audio.mp3\nMode: 0\n",
            self.smetadata,
            self.sdiff,
            "[TimingPoints]\n0,500,4,1,0,100,1,0\n",  # Základní timing (120 BPM)
            "[HitObjects]"
        ] + self.circles
        
        self.temp_file = BASE_DIR / 'temp'
        self._create_temp_file()

        filepath = BASE_DIR / f'output'
            
        path = self.temp_file / self.name
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        temp_f = BASE_DIR / 'temp' 
        shutil.make_archive(f'{filepath}', 'zip',  temp_f)
       
        os.rename(f"{filepath}.zip", f"{filepath}.osz")
        shutil.rmtree(temp_f)

if __name__ == '__main__':
    builder = OsuBuilder(title="Test", version="Hard", cs=10)
    offset = 0
    for i in range(0, 512, 16):
        for x in range(0, 384, 16):
            offset += 1
            builder.add_circle(i+8, x+8, 1000+offset)
    builder.save()
            



