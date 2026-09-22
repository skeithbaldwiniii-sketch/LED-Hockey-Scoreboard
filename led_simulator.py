# ============================================================
# led_simulator.py
#
# Windows simulator for the 64x32 hockey LED display.
#
# This file handles:
#   - Tkinter window
#   - Pixel enlargement
#   - Game polling
#   - Carousel
#   - Goal alerts
#
# All actual scoreboard drawing is handled by:
#   scoreboard_renderer.py
# ============================================================

import tkinter as tk

from led_data import get_all_games
from scoreboard_renderer import (
    WIDTH,
    HEIGHT,
    BLACK,
    render_game,
    render_goal,
    render_no_games,
)


# ============================================================
# DISPLAY SETTINGS
# ============================================================

PIXEL_SIZE = 14

WINDOW_WIDTH = WIDTH * PIXEL_SIZE
WINDOW_HEIGHT = HEIGHT * PIXEL_SIZE

DATA_REFRESH_MS = 10_000
CAROUSEL_MS = 5_000
GOAL_ALERT_MS = 8_000


# ============================================================
# SIMULATOR
# ============================================================

class LEDSimulator:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Hockey LED Scoreboard — 64x32"
        )

        self.root.resizable(
            False,
            False
        )

        # ----------------------------------------------------
        # Canvas
        # ----------------------------------------------------

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            highlightthickness=0,
            bg="#000000"
        )

        self.canvas.pack()

        # ----------------------------------------------------
        # Pixel rectangles
        #
        # Create them once and simply recolor them later.
        # ----------------------------------------------------

        self.pixels = []

        for y in range(HEIGHT):

            row = []

            for x in range(WIDTH):

                x1 = x * PIXEL_SIZE
                y1 = y * PIXEL_SIZE
                x2 = x1 + PIXEL_SIZE
                y2 = y1 + PIXEL_SIZE

                pixel = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#000000",
                    outline=""
                )

                row.append(pixel)

            self.pixels.append(row)

        # ----------------------------------------------------
        # Game state
        # ----------------------------------------------------

        self.games = []

        self.current_game_index = 0

        # ----------------------------------------------------
        # Goal alert state
        # ----------------------------------------------------

        self.goal_alert = False
        self.goal_game = None
        self.goal_data = None

        # Remember the most recently known goal for each game.
        self.known_goals = {}

        # ----------------------------------------------------
        # Start
        # ----------------------------------------------------

        self.refresh_data()

        self.root.after(
            CAROUSEL_MS,
            self.advance_carousel
        )


    # ========================================================
    # DATA
    # ========================================================

    def refresh_data(self):

        try:

            new_games = get_all_games()

            self.check_for_new_goals(
                new_games
            )

            self.games = new_games

            # Keep carousel index valid.
            if self.games:

                if self.current_game_index >= len(self.games):
                    self.current_game_index = 0

            else:

                self.current_game_index = 0

            # Don't interrupt a goal alert.
            if not self.goal_alert:
                self.draw_current_screen()

        except Exception as e:

            print(
                f"LED simulator data error: {e}"
            )

        self.root.after(
            DATA_REFRESH_MS,
            self.refresh_data
        )


    # ========================================================
    # GOAL DETECTION
    # ========================================================

    def check_for_new_goals(self, games):

        for game in games:

            game_id = game.get(
                "game_id"
            )

            goal = game.get(
                "latest_goal"
            )

            # No goal information.
            if not goal:
                continue

            goal_id = goal.get(
                "goal_id"
            )

            # Nothing usable to compare.
            if goal_id is None:
                continue

            previous_goal_id = self.known_goals.get(
                game_id
            )

            # First time seeing this game.
            #
            # Record the goal but DO NOT trigger an alert.
            if previous_goal_id is None:

                self.known_goals[game_id] = goal_id

                continue

            # New goal detected.
            if goal_id != previous_goal_id:

                self.known_goals[game_id] = goal_id

                self.start_goal_alert(
                    game,
                    goal
                )


    # ========================================================
    # GOAL ALERT
    # ========================================================

    def start_goal_alert(
        self,
        game,
        goal
    ):

        print(
            f"GOAL ALERT: "
            f"{goal.get('team')} "
            f"{goal.get('scorer')}"
        )

        self.goal_alert = True

        self.goal_game = game

        self.goal_data = goal

        self.draw_goal_screen()

        # Cancel any existing alert timer by simply scheduling
        # the new end. The latest goal alert wins.
        self.root.after(
            GOAL_ALERT_MS,
            self.end_goal_alert
        )


    def end_goal_alert(self):

        self.goal_alert = False

        self.goal_game = None

        self.goal_data = None

        self.draw_current_screen()


    # ========================================================
    # CAROUSEL
    # ========================================================

    def advance_carousel(self):

        if self.games and not self.goal_alert:

            self.current_game_index += 1

            if self.current_game_index >= len(self.games):
                self.current_game_index = 0

            self.draw_current_screen()

        self.root.after(
            CAROUSEL_MS,
            self.advance_carousel
        )


    # ========================================================
    # DRAWING
    # ========================================================

    def draw_current_screen(self):

        if not self.games:

            frame = render_no_games()

        else:

            game = self.games[
                self.current_game_index
            ]

            frame = render_game(
                game
            )

        self.draw_frame(
            frame
        )


    def draw_goal_screen(self):

        if not self.goal_game or not self.goal_data:
            return

        frame = render_goal(
            self.goal_game,
            self.goal_data
        )

        self.draw_frame(
            frame
        )


    # ========================================================
    # PIXEL OUTPUT
    # ========================================================

    def draw_frame(self, frame):

        for y in range(HEIGHT):

            for x in range(WIDTH):

                r, g, b = frame[y][x]

                color = (
                    f"#{r:02x}"
                    f"{g:02x}"
                    f"{b:02x}"
                )

                self.canvas.itemconfig(
                    self.pixels[y][x],
                    fill=color
                )


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    app = LEDSimulator(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()