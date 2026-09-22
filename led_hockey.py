# ============================================================
# led_hockey.py
#
# Physical Raspberry Pi hockey scoreboard.
#
# Data:
#     led_data.py
#
# Rendering:
#     scoreboard_renderer.py
#
# Hardware:
#     led_pi.py
#
# Display:
#     64x32 HUB75 RGB LED matrix
# ============================================================

import time

from led_data import get_all_games

from scoreboard_renderer import (
    render_game,
    render_goal,
    render_no_games,
)

from led_pi import PiLEDDisplay


# ============================================================
# SETTINGS
# ============================================================

DATA_REFRESH_SECONDS = 10
CAROUSEL_SECONDS = 5
GOAL_ALERT_SECONDS = 8


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("HOCKEY LED SCOREBOARD")
    print("=" * 60)

    print()
    print("Initializing LED display...")

    display = PiLEDDisplay()

    print("LED display initialized.")
    print()
    print("Starting hockey scoreboard...")
    print()

    games = []
    current_index = 0

    last_data_refresh = 0
    last_carousel_change = time.monotonic()

    goal_alert = None
    goal_alert_until = 0

    # Remember the most recent goal we've already displayed.
    known_goals = {}

    try:

        while True:

            now = time.monotonic()

            # ====================================================
            # REFRESH HOCKEY DATA
            # ====================================================

            if (
                now - last_data_refresh
                >= DATA_REFRESH_SECONDS
            ):

                print("Refreshing hockey data...")

                try:

                    new_games = get_all_games()

                    if new_games is None:
                        new_games = []

                    # ------------------------------------------------
                    # Detect newly scored goals.
                    # ------------------------------------------------

                    for game in new_games:

                        game_id = game.get(
                            "game_id"
                        )

                        latest_goal = game.get(
                            "latest_goal"
                        )

                        if not game_id:
                            continue

                        if not latest_goal:
                            continue

                        goal_id = latest_goal.get(
                            "goal_id"
                        )

                        if not goal_id:
                            continue

                        previous_goal = known_goals.get(
                            game_id
                        )

                        # First time seeing a live game:
                        # record the current goal without announcing it.
                        if previous_goal is None:

                            known_goals[
                                game_id
                            ] = goal_id

                            continue

                        # A different goal ID means a new goal.
                        if goal_id != previous_goal:

                            print()
                            print("!!! GOAL DETECTED !!!")

                            print(
                                game.get("league"),
                                game.get("away"),
                                game.get("away_score"),
                                "-",
                                game.get("home_score"),
                                game.get("home")
                            )

                            print(
                                "Scorer:",
                                latest_goal.get(
                                    "scorer"
                                )
                            )

                            print()

                            goal_alert = (
                                game,
                                latest_goal
                            )

                            goal_alert_until = (
                                time.monotonic()
                                + GOAL_ALERT_SECONDS
                            )

                            known_goals[
                                game_id
                            ] = goal_id

                    # ------------------------------------------------
                    # Replace current game list.
                    # ------------------------------------------------

                    games = new_games

                    # Keep index valid.
                    if games:

                        if current_index >= len(games):

                            current_index = 0

                    else:

                        current_index = 0

                    print(
                        f"Games found: {len(games)}"
                    )

                except Exception as exc:

                    print(
                        "Data refresh error:",
                        exc
                    )

                last_data_refresh = now

            # ====================================================
            # GOAL ALERT
            # ====================================================

            if (
                goal_alert is not None
                and time.monotonic()
                < goal_alert_until
            ):

                game, goal = goal_alert

                frame = render_goal(
                    game,
                    goal
                )

                display.draw_frame(frame)

                time.sleep(0.05)

                continue

            # Goal alert finished.
            if (
                goal_alert is not None
                and time.monotonic()
                >= goal_alert_until
            ):

                goal_alert = None

                # Reset carousel timing so we don't
                # immediately jump to another game.
                last_carousel_change = (
                    time.monotonic()
                )

            # ====================================================
            # NO GAMES
            # ====================================================

            if not games:

                frame = render_no_games()

                display.draw_frame(frame)

                time.sleep(0.1)

                continue

            # ====================================================
            # CAROUSEL
            # ====================================================

            if (
                time.monotonic()
                - last_carousel_change
                >= CAROUSEL_SECONDS
            ):

                current_index = (
                    current_index + 1
                ) % len(games)

                last_carousel_change = (
                    time.monotonic()
                )

            # ====================================================
            # RENDER CURRENT GAME
            # ====================================================

            game = games[current_index]

            frame = render_game(
                game
            )

            display.draw_frame(
                frame
            )

            # Small delay prevents the loop
            # from hammering the CPU.
            time.sleep(0.05)

    except KeyboardInterrupt:

        print()
        print("Stopping scoreboard...")

    finally:

        display.close()

        print("LED display cleared.")
        print("Goodbye.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()