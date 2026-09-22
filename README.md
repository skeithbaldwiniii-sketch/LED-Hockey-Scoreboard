# NHL & PWHL LED Hockey Scoreboard

A Raspberry Pi-powered RGB LED hockey scoreboard that displays live NHL
and PWHL game information on a HUB75 RGB LED matrix.

The project uses a Raspberry Pi as the production display controller,
with Windows used as the primary development and simulation environment.

## Features

-   Live NHL game scores
-   Live PWHL game scores
-   Pregame, live, and final game states
-   Team-specific display colors
-   Period and game-clock information
-   Goal detection through play-by-play data
-   Goal alert framework
-   64×32 RGB LED matrix rendering
-   Windows-based LED display simulator
-   Raspberry Pi HUB75 hardware output
-   Shared renderer between the Windows simulator and physical LED
    display

## Hardware

Current prototype:

-   Raspberry Pi 4 (4 GB)
-   Waveshare P5 RGB LED Matrix
-   64×32 pixels
-   HUB75 interface
-   5V external power supply

The LED panel is driven directly from the Raspberry Pi GPIO using the
`rpi-rgb-led-matrix` library.

## Software Architecture

``` text
NHL API ──────┐
              │
PWHL API ─────┤
              ▼
        led_data.py
              │
              ▼
   scoreboard_renderer.py
              │
       ┌──────┴──────┐
       ▼             ▼
led_simulator.py   led_hockey.py
   (Windows)          (Pi)
                         │
                         ▼
                     led_pi.py
                         │
                         ▼
                    HUB75 Panel
```

The data layer and renderer are shared between development and
production. Hardware-specific functionality is isolated in the Raspberry
Pi display backend.

## Development

Windows is used for development and testing.

The included simulator provides a software representation of the 64×32
LED display, allowing scoreboard layouts and rendering changes to be
tested without the physical hardware.

Install the Python dependencies:

``` bash
pip install -r requirements.txt
```

Run the simulator:

``` bash
python led_simulator.py
```

## Raspberry Pi

The physical scoreboard runs on Raspberry Pi OS and uses
[`rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix) to
drive the HUB75 display.

The Raspberry Pi installation requires the additional dependencies and
configuration described by the `rpi-rgb-led-matrix` project.

The physical display is launched with:

``` bash
sudo .venv/bin/python led_hockey.py
```

## Current Display

The scoreboard currently renders game information within a 64×32 pixel
display area.

The renderer is designed around the constraints of a low-resolution LED
matrix, using compact bitmap fonts and abbreviated team names.

## Roadmap

Planned improvements include:

-   Display goal scorer using first initial and last name
-   Scheduled operating hours
-   Automatic startup after Raspberry Pi reboot
-   Automatic recovery if the scoreboard application stops
-   Support for multiple chained LED panels
-   Additional game statistics
-   Expanded goal animations
-   Additional NHL and PWHL display modes

## Project Status

The project currently has a functioning physical prototype running on a
Raspberry Pi and HUB75 RGB LED matrix.
