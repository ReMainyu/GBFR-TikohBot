# GBFR Grinding Assistant

This script is designed to alleviate the repetitive aspect of GBFR and apply some QoL measures using Python. It supports automation and shortcuts to enhance the experience and to eliminate Carpal Tunnel Syndrome.

Updated for game version v1.2.

## Features

- Automates perfect Rackam's shots in any quest, but works best in Slimepede.
- Using fast travel to interact with NPCs.
- Moving into one of the four designated positions in Slimepede and begin automatic fire.
- Full auto mode:
  - Travels to the Quest Counter, select and start the Slimepede quest. Moves into the back upon quest entry and begin automatic fire.
  - Will continue to move into position and automatic fire but you have to turn on repeat manually.
- Skips chest opening and reduce quest result to 5s.
- Repeat quest indefinitely.

## Disclaimer

Script has been tested in closed matchmaking and offline mode.

Timer for macros are tested on 60FPS, and will have a different result at 30FPS or 120FPS.

## Setup

Install [Python] if you don't have it on your system.
Open up the command prompt(cmd) and run the following commands to install the dependencies:
```sh
pip install -r requirements.txt
```
__Always__ run GBFR first before the script.

Go to Game Options > Gameplay.
- Ensure "Quest Cutscene Auto-Skip" is set to __On__ and "Loading Screen Skip" is set to __Auto Skip__.

See Controls.

## Controls

- F1: Activates automatic fire for Rackam.
- F2: Moves to one of the four designated positions before activating automatic fire.
- F3: Travels to the Quest Counter, select and start the Slimepede repeat. Moves into the back upon repeat entry and begins Automatic fire. Combine with F5 & F6 for the best experience.
- F5: Toggle skip chest and reward timer.
- F6: Toggle quest repeat.
- r + 1: Fast travel to move and interact with the Quest Counter and talk to the NPC.
- r + 2: Fast travel to move and interact with the Blacksmith.
- r + 3: Fast travel to move and interact with Sierokarte.
- r + 4: Fast travel to move and interact with Zathba.
- Ctrl + q: Force quits the script.

[Python]: <https://www.python.org/downloads>