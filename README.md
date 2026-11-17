# Stormlight Harbor — Student Workshop

Build a side-scrolling platformer with Python and Kraken Engine. Finish the map in Tiled, fix two gameplay bugs, implement jumping and gravity, animate the Tide Warden with Orchestrator, and add sound effects and streamed music.

## Run

Install Python 3.11 or newer. Download or clone this repository, open its folder in a terminal, then:

```sh
python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python play.py
```

The starter intentionally has missing features and bugs. Follow [the 90-minute worksheet](docs/LESSON.md). The supplied game framework handles rendering, collision, boss attacks, checkpoints and respawning.

## Your files

- `student/harbor.tmx`: open in Tiled to build the unfinished route.
- `student/movement.py`: fix direction and hit protection; implement gravity and jumping.
- `student/boss_animation.py`: implement the boss's visual animation timeline.
- `student/audio.py`: load and play samples and a looping music stream.
- `docs/API_NOTES.md`: offline API excerpts, alongside links in the worksheet.

Paint solid tiles on **Platforms** and decoration on **Scenery**. Tile collision follows Platforms automatically. Preserve the map's layer names and CSV tile encoding. Save and restart the game after editing.

Controls: A/D or arrows move, Space jumps, J shoots, R resets, B opens Boss Lab, M mutes, Escape closes. Some controls require completing the exercises first. In Boss Lab the attacks already work; shoot when the shield is down, then reach the exit.

## Assets and license

All required textures, animation frames, tile maps, sounds, music and MIDI are included. Kenney Pixel Platformer artwork is CC0; see [asset credits](ASSET_CREDITS.md). Original code and audio are MIT licensed. Runtime dependency: Kraken Engine 1.8.0.
