# Kar Topu Savaşı (Snowball Fight)

A mobile game built with Python using Kivy/KivyMD framework.

## Features

- Side-scrolling snowball fight game
- Character selection with unique abilities
- Mobile-optimized touch controls
- Desktop keyboard support
- Turkish language interface
- Android packaging support

## Requirements

- Python 3.8+
- Kivy 2.3.0+
- KivyMD 1.1.1+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Karyazilim/7AKartopu.git
cd 7AKartopu
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

### Desktop
```bash
python app/main.py
```

### Android Build

1. Install Buildozer:
```bash
pip install buildozer
```

2. Build APK:
```bash
buildozer android debug
```

The APK will be generated in the `bin/` directory.

## Controls

### Desktop
- **Movement**: Arrow keys or A/D
- **Jump**: Space or W
- **Throw**: F key

### Mobile
- Use on-screen touch controls

## Characters

- **Arda**: Faster movement speed
- **Elif**: Shorter throw cooldown
- **Can**: Heavier snowballs with more knockback
- **Ayşe**: Higher jump ability

## Game Rules

- 60-second timer
- Hit enemies with snowballs to score points
- Avoid enemy snowballs
- Game ends when timer reaches zero

## License

MIT License - see LICENSE file for details.