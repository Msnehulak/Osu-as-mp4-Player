import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"


class OsuBuilder:
    def __init__(
        self,
        title="Song",
        artist="Artist",
        creator="Bot",
        version="Normal",
        cs: float = 5.0,
        hp: float = 5.0,
        od: float = 5.0,
        ar: float = 8.0,
    ):
        self.metadata = {
            "title": title,
            "artist": artist,
            "creator": creator,
            "version": version,
        }
        self.diff = {"cs": cs, "hp": hp, "od": od, "ar": ar}
        self.circles = []
        self.audio_path: Path | None = None
        self._update_map_data()

    def add_audio(self, audio_path: Path):
        """Uloží cestu k audio souboru, který se zkopíruje do temp složky."""
        self.audio_path = Path(audio_path)

    def _update_map_data(self):
        general = (
            "[General]",
            "AudioFilename: audio.mp3",
            "Mode: 0",
            "StackLeniency:0",
        )

        md = self.metadata
        self.map_name = (
            f"{md['artist']} - {md['title']} ({md['creator']}) [{md['version']}].osu"
        )
        metadata = [
            "[Metadata]",
            f"Title:{md['title']}",
            f"Artist:{md['artist']}",
            f"Creator:{md['creator']}",
            f"Version:{md['version']}",
        ]

        dd = self.diff
        diff = [
            "[Difficulty]",
            f"HPDrainRate:{dd['hp']:.1f}",
            f"CircleSize:{dd['cs']:.1f}",
            f"OverallDifficulty:{dd['od']:.1f}",
            f"ApproachRate:{dd['ar']:.1f}",
            "SliderMultiplier:1.4",
            "SliderTickRate:1",
        ]

        self.content = [
            "osu file format v14\n",
            f"{'\n'.join(general)}",
            f"{'\n'.join(metadata)}",
            f"{'\n'.join(diff)}",
            "[TimingPoints]\n0,500,4,1,0,100,1,0\n",
            "[HitObjects]",
        ] + self.circles

    def add_circle(self, x: int, y: int, time_ms: int):
        self.circles.append(f"{x},{y},{time_ms},1,0,0:0:0:0:")

    def _create_temp_file(self):
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

    def save(self, name: str):
        self._update_map_data()
        self._create_temp_file()

        # Pokud bylo předáno audio, překopíruje se do tempu jako audio.mp3
        if self.audio_path and self.audio_path.exists():
            shutil.copy(self.audio_path, TEMP_DIR / "audio.mp3")
        else:
            print("Varování: Audio soubor nebyl nalezen nebo přidán!")

        filepath = BASE_DIR / name

        path = TEMP_DIR / self.map_name
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.content))

        shutil.make_archive(f"{filepath}", "zip", TEMP_DIR)

        os.rename(f"{filepath}.zip", f"{filepath}.osz")
        shutil.rmtree(TEMP_DIR)
