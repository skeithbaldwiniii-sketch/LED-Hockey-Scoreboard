# ============================================================
# led_renderer.py
# 64x32 Pixel-Accurate Hockey LED Scoreboard Simulator
# ============================================================

import tkinter as tk

from led_data import get_all_games


# ============================================================
# PHYSICAL DISPLAY
# ============================================================

WIDTH = 64
HEIGHT = 32

PIXEL_SIZE = 14

WINDOW_WIDTH = WIDTH * PIXEL_SIZE
WINDOW_HEIGHT = HEIGHT * PIXEL_SIZE


# ============================================================
# TIMING
# ============================================================

DATA_REFRESH_MS = 10000
GAME_DISPLAY_MS = 5000
GOAL_ALERT_MS = 8000


# ============================================================
# COLORS
# ============================================================

BLACK = "#000000"
WHITE = "#FFFFFF"
GRAY = "#777777"


TEAM_COLORS = {

    # NHL
    "NHL_ANA": "#F47A38",
    "NHL_UTA": "#AFA0FF",
    "NHL_BOS": "#FFB81C",
    "NHL_BUF": "#003087",
    "NHL_CGY": "#C8102E",
    "NHL_CAR": "#CC0000",
    "NHL_CHI": "#CF0A2C",
    "NHL_COL": "#6F263D",
    "NHL_CBJ": "#002654",
    "NHL_DAL": "#006847",
    "NHL_DET": "#CE1126",
    "NHL_EDM": "#FF4C00",
    "NHL_FLA": "#C8102E",
    "NHL_LAK": "#AAAAAA",
    "NHL_MIN": "#154734",
    "NHL_MTL": "#AF1E2D",
    "NHL_NSH": "#FFB81C",
    "NHL_NJD": "#CE1126",
    "NHL_NYI": "#00539B",
    "NHL_NYR": "#0038A8",
    "NHL_OTT": "#C52032",
    "NHL_PHI": "#F74902",
    "NHL_PIT": "#FCB514",
    "NHL_SJS": "#006D75",
    "NHL_SEA": "#7FDBFF",
    "NHL_STL": "#002F87",
    "NHL_TBL": "#002868",
    "NHL_TOR": "#4A90E2",
    "NHL_VAN": "#00205B",
    "NHL_VGK": "#B4975A",
    "NHL_WSH": "#C8102E",
    "NHL_WPG": "#041E42",

    # PWHL
    "PWHL_BOS": "#006847",
    "PWHL_MIN": "#5B2C83",
    "PWHL_MTL": "#6CACE4",
    "PWHL_NY": "#1D428A",
    "PWHL_OTT": "#8B1538",
    "PWHL_TOR": "#4B2E83"
}


# ============================================================
# 5x7 FONT
# ============================================================

FONT_5X7 = {

    "A": [
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001"
    ],

    "B": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110"
    ],

    "C": [
        "01111",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "01111"
    ],

    "D": [
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110"
    ],

    "E": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111"
    ],

    "F": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "10000"
    ],

    "G": [
        "01111",
        "10000",
        "10000",
        "10111",
        "10001",
        "10001",
        "01111"
    ],

    "H": [
        "10001",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001"
    ],

    "I": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "11111"
    ],

    "J": [
        "00111",
        "00010",
        "00010",
        "00010",
        "00010",
        "10010",
        "01100"
    ],

    "K": [
        "10001",
        "10010",
        "10100",
        "11000",
        "10100",
        "10010",
        "10001"
    ],

    "L": [
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111"
    ],

    "M": [
        "10001",
        "11011",
        "10101",
        "10101",
        "10001",
        "10001",
        "10001"
    ],

    "N": [
        "10001",
        "11001",
        "11001",
        "10101",
        "10011",
        "10011",
        "10001"
    ],

    "O": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110"
    ],

    "P": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10000",
        "10000",
        "10000"
    ],

    "Q": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10101",
        "10010",
        "01101"
    ],

    "R": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10100",
        "10010",
        "10001"
    ],

    "S": [
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110"
    ],

    "T": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100"
    ],

    "U": [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110"
    ],

    "V": [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01010",
        "00100"
    ],

    "W": [
        "10001",
        "10001",
        "10001",
        "10101",
        "10101",
        "11011",
        "10001"
    ],

    "X": [
        "10001",
        "10001",
        "01010",
        "00100",
        "01010",
        "10001",
        "10001"
    ],

    "Y": [
        "10001",
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "00100"
    ],

    "Z": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "10000",
        "11111"
    ],

    "0": [
        "01110",
        "10001",
        "10011",
        "10101",
        "11001",
        "10001",
        "01110"
    ],

    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110"
    ],

    "2": [
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111"
    ],

    "3": [
        "11110",
        "00001",
        "00001",
        "01110",
        "00001",
        "00001",
        "11110"
    ],

    "4": [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010"
    ],

    "5": [
        "11111",
        "10000",
        "10000",
        "11110",
        "00001",
        "00001",
        "11110"
    ],

    "6": [
        "01110",
        "10000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110"
    ],

    "7": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000"
    ],

    "8": [
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110"
    ],

    "9": [
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00001",
        "01110"
    ],

    ":": [
        "00000",
        "00100",
        "00100",
        "00000",
        "00100",
        "00100",
        "00000"
    ],

    "-": [
        "00000",
        "00000",
        "00000",
        "11111",
        "00000",
        "00000",
        "00000"
    ],

    "@": [
        "01110",
        "10001",
        "10111",
        "10101",
        "10111",
        "10000",
        "01110"
    ],

    "!": [
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00000",
        "00100"
    ],

    ".": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00110",
        "00110"
    ],

    "/": [
        "00001",
        "00010",
        "00010",
        "00100",
        "01000",
        "01000",
        "10000"
    ],

    " ": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000"
    ]
}


# ============================================================
# 3x5 FONT
#
# Used for long player names / assist lines.
# ============================================================

FONT_3X5 = {

    "A": ["010", "101", "111", "101", "101"],
    "B": ["110", "101", "110", "101", "110"],
    "C": ["011", "100", "100", "100", "011"],
    "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"],
    "F": ["111", "100", "110", "100", "100"],
    "G": ["011", "100", "101", "101", "011"],
    "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "J": ["001", "001", "001", "101", "010"],
    "K": ["101", "101", "110", "101", "101"],
    "L": ["100", "100", "100", "100", "111"],
    "M": ["10001", "11011", "10101", "10101", "10101"],
    "N": ["101", "111", "111", "111", "101"],
    "O": ["010", "101", "101", "101", "010"],
    "P": ["110", "101", "110", "100", "100"],
    "Q": ["010", "101", "101", "011", "001"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"],
    "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "010"],
    "V": ["101", "101", "101", "101", "010"],
    "W": ["101", "101", "111", "111", "101"],
    "X": ["101", "101", "010", "101", "101"],
    "Y": ["101", "101", "010", "010", "010"],
    "Z": ["111", "001", "010", "100", "111"],

    "0": ["111", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "111"],
    "2": ["110", "001", "010", "100", "111"],
    "3": ["110", "001", "010", "001", "110"],
    "4": ["101", "101", "111", "001", "001"],
    "5": ["111", "100", "110", "001", "110"],
    "6": ["011", "100", "111", "101", "111"],
    "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"],
    "9": ["111", "101", "111", "001", "110"],

    ":": ["000", "010", "000", "010", "000"],
    "-": ["000", "000", "111", "000", "000"],
    "@": ["010", "101", "111", "100", "011"],
    "!": ["010", "010", "010", "000", "010"],
    "/": ["001", "001", "010", "100", "100"],
    ".": ["000", "000", "000", "011", "011"],
    " ": ["000", "000", "000", "000", "000"]
}


# ============================================================
# SIMULATOR
# ============================================================

class LEDSimulator:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "Hockey LED Scoreboard — 64x32"
        )

        self.root.configure(
            bg=BLACK
        )

        self.root.resizable(
            False,
            False
        )


        # ====================================================
        # CANVAS
        # ====================================================

        self.canvas = tk.Canvas(

            self.root,

            width=WINDOW_WIDTH,

            height=WINDOW_HEIGHT,

            bg=BLACK,

            highlightthickness=0
        )

        self.canvas.pack()


        # ====================================================
        # STATE
        # ====================================================

        self.games = []

        self.game_index = 0

        self.last_goal_ids = {}

        self.goal_alert_active = False

        self.current_goal = None

        self.current_goal_game = None


        # ====================================================
        # INITIAL DATA
        # ====================================================

        self.refresh_data()

        self.root.mainloop()


    # ========================================================
    # DATA REFRESH
    # ========================================================

    def refresh_data(self):

        try:

            new_games = get_all_games()

        except Exception as e:

            print(
                f"Data error: {e}"
            )

            new_games = []


        self.process_new_games(
            new_games
        )


        self.games = new_games


        if self.games:

            if self.game_index >= len(
                self.games
            ):

                self.game_index = 0

        else:

            self.game_index = 0


        if not self.goal_alert_active:

            self.render_current_game()


        self.root.after(
            DATA_REFRESH_MS,
            self.refresh_data
        )


    # ========================================================
    # NEW GOAL DETECTION
    # ========================================================

    def process_new_games(
        self,
        games
    ):

        for game in games:

            game_id = game[
                "game_id"
            ]

            latest_goal = game.get(
                "latest_goal"
            )


            if not latest_goal:

                continue


            goal_id = latest_goal.get(
                "goal_id"
            )


            if goal_id is None:

                continue


            if game_id not in self.last_goal_ids:

                self.last_goal_ids[
                    game_id
                ] = goal_id

                continue


            if (
                self.last_goal_ids[
                    game_id
                ]
                != goal_id
            ):

                self.last_goal_ids[
                    game_id
                ] = goal_id


                self.trigger_goal_alert(
                    game,
                    latest_goal
                )


    # ========================================================
    # GOAL ALERT
    # ========================================================

    def trigger_goal_alert(
        self,
        game,
        goal
    ):

        print()

        print(
            "========================================"
        )

        print(
            "GOAL ALERT"
        )

        print(
            f"{game['league']} | "
            f"{game['away']} @ "
            f"{game['home']}"
        )

        print(
            f"GOAL: "
            f"{goal['team']} - "
            f"{goal['scorer']}"
        )

        if goal["assists"]:

            print(
                "ASSISTS: "
                + ", ".join(
                    goal["assists"]
                )
            )

        print(
            "========================================"
        )


        self.current_goal = goal

        self.current_goal_game = game

        self.goal_alert_active = True


        self.draw_goal_alert()


        self.root.after(
            GOAL_ALERT_MS,
            self.end_goal_alert
        )


    # ========================================================
    # END GOAL ALERT
    # ========================================================

    def end_goal_alert(self):

        self.goal_alert_active = False

        self.current_goal = None

        self.current_goal_game = None

        self.render_current_game()


    # ========================================================
    # NORMAL DISPLAY
    # ========================================================

    def render_current_game(self):

        if self.goal_alert_active:

            return


        self.clear_display()


        if not self.games:

            self.draw_text_center(
                "NO GAMES",
                14,
                FONT_5X7,
                WHITE
            )

            return


        game = self.games[
            self.game_index
        ]


        status = game[
            "status"
        ]


        if status == "PREGAME":

            self.draw_pregame(
                game
            )

        elif status == "LIVE":

            self.draw_live(
                game
            )

        elif status == "FINAL":

            self.draw_final(
                game
            )

        else:

            self.draw_text_center(
                "UNKNOWN",
                14,
                FONT_5X7,
                WHITE
            )


        self.root.after(
            GAME_DISPLAY_MS,
            self.next_game
        )


    # ========================================================
    # NEXT GAME
    # ========================================================

    def next_game(self):

        if self.goal_alert_active:

            return


        if not self.games:

            return


        self.game_index += 1


        if self.game_index >= len(
            self.games
        ):

            self.game_index = 0


        self.render_current_game()


    # ========================================================
    # PREGAME
    # ========================================================

    def draw_pregame(
        self,
        game
    ):

        league = game["league"]

        away = game["away"]

        home = game["home"]

        start_time = game["start_time"]


        self.draw_text_center(
            league,
            2,
            FONT_5X7,
            WHITE
        )


                # ====================================================
        # MATCHUP
        # ====================================================

        self.draw_text_center(
            away,
            13,
            FONT_5X7,
            self.team_color(
                league,
                away
            ),
            x=10
        )

        self.draw_text_center(
            "@",
            13,
            FONT_3X5,
            WHITE,
            x=32
        )

        self.draw_text_center(
            home,
            13,
            FONT_5X7,
            self.team_color(
                league,
                home
            ),
            x=54
        )

        if start_time:

            self.draw_text_center(
                start_time,
                25,
                FONT_5X7,
                WHITE
            )


    # ========================================================
    # LIVE
    # ========================================================

    def draw_live(
        self,
        game
    ):

        league = game["league"]

        away = game["away"]

        home = game["home"]

        away_score = str(
            game["away_score"]
        )

        home_score = str(
            game["home_score"]
        )


        self.draw_text_center(
            league,
            1,
            FONT_5X7,
            WHITE
        )


        self.draw_text_center(
            away,
            12,
            FONT_5X7,
            self.team_color(
                league,
                away
            ),
            x=10
        )


        self.draw_text_center(
            away_score,
            12,
            FONT_5X7,
            WHITE,
            x=23
        )


        self.draw_text_center(
            "-",
            12,
            FONT_5X7,
            WHITE,
            x=32
        )


        self.draw_text_center(
            home_score,
            12,
            FONT_5X7,
            WHITE,
            x=41
        )


        self.draw_text_center(
            home,
            12,
            FONT_5X7,
            self.team_color(
                league,
                home
            ),
            x=54
        )


        period = game["period"]

        clock = game["clock"]


        if period is not None:

            if clock:

                status = (
                    f"P{period} {clock}"
                )

            else:

                status = f"P{period}"


            self.draw_text_center(
                status,
                23,
                FONT_5X7,
                WHITE
            )


    # ========================================================
    # FINAL
    # ========================================================

    def draw_final(
        self,
        game
    ):

        league = game["league"]

        away = game["away"]

        home = game["home"]

        away_score = str(
            game["away_score"]
        )

        home_score = str(
            game["home_score"]
        )


        self.draw_text_center(
            f"{league} FINAL",
            2,
            FONT_5X7,
            WHITE
        )


        self.draw_text_center(
            away,
            14,
            FONT_5X7,
            self.team_color(
                league,
                away
            ),
            x=10
        )


        self.draw_text_center(
            away_score,
            14,
            FONT_5X7,
            WHITE,
            x=25
        )


        self.draw_text_center(
            "-",
            14,
            FONT_5X7,
            WHITE,
            x=32
        )


        self.draw_text_center(
            home_score,
            14,
            FONT_5X7,
            WHITE,
            x=39
        )


        self.draw_text_center(
            home,
            14,
            FONT_5X7,
            self.team_color(
                league,
                home
            ),
            x=53
        )


    # ========================================================
    # GOAL ALERT
    # ========================================================

    def draw_goal_alert(self):

        self.clear_display()


        game = self.current_goal_game

        goal = self.current_goal


        if not game or not goal:

            return


        league = game["league"]

        team = goal["team"]

        scorer = goal["scorer"]

        assists = goal["assists"]


        # ====================================================
        # GOAL
        # ====================================================

        self.draw_text_center(
            "GOAL!",
            2,
            FONT_5X7,
            WHITE
        )


        # ====================================================
        # TEAM
        # ====================================================

        self.draw_text_center(
            team,
            10,
            FONT_5X7,
            self.team_color(
                league,
                team
            )
        )


        # ====================================================
        # SCORER
        # ====================================================

        scorer_text = scorer.upper()


        if self.text_width(
            scorer_text,
            FONT_3X5
        ) > WIDTH - 2:

            scorer_text = self.fit_text(
                scorer_text,
                FONT_3X5,
                WIDTH - 2
            )


        self.draw_text_center(
            scorer_text,
            16,
            FONT_3X5,
            WHITE
        )


        # ====================================================
        # ASSISTS
        # ====================================================

        if assists:

            assist_text = (
                "A: "
                + " / ".join(
                    assists
                )
            ).upper()


            if self.text_width(
                assist_text,
                FONT_3X5
            ) > WIDTH - 2:

                assist_text = self.fit_text(
                    assist_text,
                    FONT_3X5,
                    WIDTH - 2
                )


            self.draw_text_center(
                assist_text,
                21,
                FONT_3X5,
                WHITE
            )


        # ====================================================
        # TIME
        # ====================================================

        period = goal.get(
            "period"
        )

        time = goal.get(
            "time"
        )


        if period is not None and time:

            self.draw_text_center(
                f"P{period} {time}",
                27,
                FONT_3X5,
                WHITE
            )


    # ========================================================
    # TEAM COLOR
    # ========================================================

    def team_color(
        self,
        league,
        team
    ):

        return TEAM_COLORS.get(
            f"{league}_{team}",
            WHITE
        )


    # ========================================================
    # CLEAR DISPLAY
    # ========================================================

    def clear_display(self):

        self.canvas.delete(
            "all"
        )


        # Draw the individual LED pixels.

        for y in range(
            HEIGHT
        ):

            for x in range(
                WIDTH
            ):

                self.canvas.create_rectangle(

                    x * PIXEL_SIZE,

                    y * PIXEL_SIZE,

                    (x + 1) * PIXEL_SIZE,

                    (y + 1) * PIXEL_SIZE,

                    fill=BLACK,

                    outline="#111111"
                )


    # ========================================================
    # DRAW PIXEL
    # ========================================================

    def draw_pixel(
        self,
        x,
        y,
        color
    ):

        if (
            x < 0
            or x >= WIDTH
            or y < 0
            or y >= HEIGHT
        ):

            return


        self.canvas.create_rectangle(

            x * PIXEL_SIZE,

            y * PIXEL_SIZE,

            (x + 1) * PIXEL_SIZE,

            (y + 1) * PIXEL_SIZE,

            fill=color,

            outline="#111111"
        )


    # ========================================================
    # DRAW TEXT
    # ========================================================

    def draw_text(
        self,
        text,
        x,
        y,
        font,
        color
    ):

        cursor_x = x


        for character in text.upper():

            glyph = font.get(
                character,
                font.get(" ")
            )


            if not glyph:

                continue


            for row, line in enumerate(
                glyph
            ):

                for col, value in enumerate(
                    line
                ):

                    if value == "1":

                        self.draw_pixel(
                            cursor_x + col,
                            y + row,
                            color
                        )


            cursor_x += (
                len(glyph[0]) + 1
            )


    # ========================================================
    # DRAW CENTERED TEXT
    # ========================================================

    def draw_text_center(
        self,
        text,
        y,
        font,
        color,
        x=None
    ):

        width = self.text_width(
            text,
            font
        )


        if x is None:

            x = (
                WIDTH - width
            ) // 2

        else:

            x -= width // 2


        self.draw_text(
            text,
            x,
            y,
            font,
            color
        )


    # ========================================================
    # TEXT WIDTH
    # ========================================================

    def text_width(
        self,
        text,
        font
    ):

        if not text:

            return 0


        widths = []


        for character in text.upper():

            glyph = font.get(
                character,
                font.get(" ")
            )


            if glyph:

                widths.append(
                    len(glyph[0]) + 1
                )


        if not widths:

            return 0


        return sum(
            widths
        ) - 1


    # ========================================================
    # FIT TEXT
    # ========================================================

    def fit_text(
        self,
        text,
        font,
        max_width
    ):

        result = ""


        for character in text:

            candidate = (
                result + character
            )


            if self.text_width(
                candidate,
                font
            ) > max_width:

                break


            result = candidate


        return result


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    LEDSimulator()