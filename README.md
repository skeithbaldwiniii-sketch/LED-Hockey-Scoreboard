# NHL & PWHL LED Hockey Scoreboard

A Raspberry Pi-powered RGB LED hockey scoreboard that displays live NHL and PWHL game information on a HUB75 RGB LED matrix.

The project uses a Raspberry Pi as the production display controller, with Windows used as the primary development and simulation environment.

## Features

- Live NHL game scores
- Live PWHL game scores
- Pregame, live, and final game states
- Team-specific display colors
- Period and game-clock information
- Goal detection through play-by-play data
- Goal alert display
- Previous-day final scores
- Scheduled display operation
- Morning results display
- 64×32 RGB LED matrix rendering
- Windows-based LED display simulator
- Raspberry Pi HUB75 hardware output
- Shared renderer between the Windows simulator and physical LED display
- Automatic startup after Raspberry Pi reboot
- Automatic application restart through systemd

## Hardware

Current prototype:

- Raspberry Pi 4 Model B (4 GB)
- Waveshare RGB-Matrix-P5-64x32
- 64×32 RGB pixels
- HUB75 interface
- 5V / 4A external power supply

The LED panel is driven directly from the Raspberry Pi GPIO using the `rpi-rgb-led-matrix` library.

The panel uses the FM6127 driver configuration.

## Software Architecture

```text
NHL API ──────┐
              │
PWHL API ─────┤
              ▼
         led_data.py
              │
              ▼
    scoreboard_renderer.py
              │
        ┌─────┴─────┐
        ▼           ▼
led_simulator.py  led_hockey.py
   (Windows)          (Pi)
                       │
                       ▼
                   led_pi.py
                       │
                       ▼
                  HUB75 Panel
```

The data layer and renderer are shared between development and production. Hardware-specific functionality is isolated in the Raspberry Pi display backend.

## Display Scheduling

The production Raspberry Pi uses a scheduler to determine which display mode should be active.

### Weekdays

| Time | Mode |
|---|---|
| 12:00 AM – 12:59 AM | Live |
| 1:00 AM – 5:59 AM | Off |
| 6:00 AM – 6:59 AM | Morning results |
| 7:00 AM – 3:59 PM | Off |
| 4:00 PM – 11:59 PM | Live |

### Weekends

| Time | Mode |
|---|---|
| 12:00 AM – 12:59 AM | Live |
| 1:00 AM – 7:59 AM | Off |
| 8:00 AM – 11:59 PM | Live |

All scheduling uses the `America/New_York` timezone.

## Development

Windows is used for development and testing.

The included simulator provides a software representation of the 64×32 LED display, allowing scoreboard layouts and rendering changes to be tested without the physical hardware.

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run the simulator:

```bash
python led_simulator.py
```

## Raspberry Pi

The physical scoreboard runs on Raspberry Pi OS and uses [`rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix) to drive the HUB75 display.

The Raspberry Pi installation requires the additional dependencies and configuration described by the `rpi-rgb-led-matrix` project.

### Manual launch

The scoreboard can be launched manually from the project directory:

```bash
sudo .venv/bin/python led_hockey.py
```

### Production service

The production scoreboard runs as a systemd service and starts automatically after Raspberry Pi boot.

Check the service:

```bash
sudo systemctl status hockey-scoreboard
```

Restart the scoreboard:

```bash
sudo systemctl restart hockey-scoreboard
```

View the live service log:

```bash
sudo journalctl -u hockey-scoreboard -f
```

## Current Display

The scoreboard currently renders game information within a 64×32 pixel display area.

The renderer is designed around the constraints of a low-resolution LED matrix, using compact bitmap fonts and abbreviated team names.

The physical display currently supports:

- Pregame displays
- Live game displays
- Final scores
- Goal alerts
- Morning results
- Scheduled off/dark periods

## Project Status

The project currently has a functioning physical scoreboard running independently on a Raspberry Pi 4 and HUB75 RGB LED matrix.

The production system supports NHL and PWHL game data, scheduled operation, morning results, goal detection, automatic startup after reboot, and automatic application restart.

Windows provides the primary development and simulation environment, while the Raspberry Pi serves as the standalone production display controller.

## Roadmap

Planned improvements include:

- Support for multiple chained LED panels
- Additional game statistics
- Expanded goal animations
- Additional NHL and PWHL display modes
- Team logos
- Live score ticker
- Shot heatmaps
- Puck path visualization
- Broadcast-oriented display modes
