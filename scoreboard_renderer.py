# ============================================================
# scoreboard_renderer.py
#
# Pure 64x32 scoreboard rendering.
#
# This file knows NOTHING about:
#   - Tkinter
#   - Raspberry Pi
#   - rgbmatrix
#   - APIs
#
# It simply turns game data into a 64x32 RGB pixel buffer.
# ============================================================

WIDTH = 64
HEIGHT = 32


# ============================================================
# COLORS
# ============================================================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 120, 0)


# ============================================================
# TEAM COLORS
#
# These can be expanded as needed.
# ============================================================

TEAM_COLORS = {

    # NHL
    "ANA": (252, 76, 0),
    "BOS": (255, 184, 0),
    "BUF": (0, 38, 84),
    "CGY": (200, 16, 46),
    "CAR": (204, 0, 0),
    "CHI": (207, 10, 44),
    "COL": (109, 32, 119),
    "CBJ": (0, 38, 84),
    "DAL": (0, 104, 71),
    "DET": (206, 17, 38),
    "EDM": (252, 76, 0),
    "FLA": (200, 16, 46),
    "LAK": (162, 170, 173),
    "MIN": (21, 71, 52),
    "MTL": (175, 30, 45),
    "NSH": (255, 184, 28),
    "NJD": (206, 17, 38),
    "NYI": (0, 83, 155),
    "NYR": (0, 56, 168),
    "OTT": (196, 18, 48),
    "PHI": (247, 73, 2),
    "PIT": (252, 181, 20),
    "SEA": (153, 214, 214),
    "SJS": (0, 109, 117),
    "STL": (0, 47, 135),
    "TBL": (0, 40, 104),
    "TOR": (0, 32, 91),
    "UTA": (105, 45, 134),
    "VAN": (0, 88, 122),
    "VGK": (185, 151, 91),
    "WSH": (200, 16, 46),
    "WPG": (4, 30, 66),

    # PWHL
    "BOS_PWHL": (0, 0, 0),
    "MIN_PWHL": (21, 71, 52),
    "MTL_PWHL": (175, 30, 45),
    "NY_PWHL": (0, 83, 155),
    "OTT_PWHL": (196, 18, 48),
    "TOR_PWHL": (0, 32, 91),
    "VAN_PWHL": (0, 88, 122),
    "SEA_PWHL": (153, 214, 214),
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
        "10001",
    ],

    "B": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110",
    ],

    "C": [
        "01111",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "01111",
    ],

    "D": [
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110",
    ],

    "E": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111",
    ],

    "F": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "10000",
    ],

    "G": [
        "01111",
        "10000",
        "10000",
        "10111",
        "10001",
        "10001",
        "01111",
    ],

    "H": [
        "10001",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],

    "I": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "11111",
    ],

    "J": [
        "00111",
        "00010",
        "00010",
        "00010",
        "00010",
        "10010",
        "01100",
    ],

    "K": [
        "10001",
        "10010",
        "10100",
        "11000",
        "10100",
        "10010",
        "10001",
    ],

    "L": [
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111",
    ],

    "M": [
        "10001",
        "11011",
        "10101",
        "10101",
        "10001",
        "10001",
        "10001",
    ],

    "N": [
        "10001",
        "11001",
        "11001",
        "10101",
        "10011",
        "10011",
        "10001",
    ],

    "O": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],

    "P": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10000",
        "10000",
        "10000",
    ],

    "Q": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10101",
        "10010",
        "01101",
    ],

    "R": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10100",
        "10010",
        "10001",
    ],

    "S": [
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110",
    ],

    "T": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ],

    "U": [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],

    "V": [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01010",
        "00100",
    ],

    "W": [
        "10001",
        "10001",
        "10001",
        "10101",
        "10101",
        "11011",
        "10001",
    ],

    "X": [
        "10001",
        "10001",
        "01010",
        "00100",
        "01010",
        "10001",
        "10001",
    ],

    "Y": [
        "10001",
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "00100",
    ],

    "Z": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "10000",
        "11111",
    ],

    "0": [
        "01110",
        "10001",
        "10011",
        "10101",
        "11001",
        "10001",
        "01110",
    ],

    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ],

    "2": [
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111",
    ],

    "3": [
        "11110",
        "00001",
        "00001",
        "01110",
        "00001",
        "00001",
        "11110",
    ],

    "4": [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010",
    ],

    "5": [
        "11111",
        "10000",
        "10000",
        "11110",
        "00001",
        "00001",
        "11110",
    ],

    "6": [
        "01110",
        "10000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110",
    ],

    "7": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000",
    ],

    "8": [
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110",
    ],

    "9": [
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00001",
        "01110",
    ],

    "!": [
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00000",
        "00100",
    ],

    "-": [
        "00000",
        "00000",
        "00000",
        "11111",
        "00000",
        "00000",
        "00000",
    ],

    ":": [
        "00000",
        "00100",
        "00100",
        "00000",
        "00100",
        "00100",
        "00000",
    ],

    ".": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00110",
        "00110",
    ],

    "@": [
        "01110",
        "10001",
        "10111",
        "10101",
        "10111",
        "10000",
        "01110",
    ],

    "/": [
        "00001",
        "00010",
        "00010",
        "00100",
        "01000",
        "01000",
        "10000",
    ],

    " ": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
    ],
}


# ============================================================
# 3x5 FONT
#
# Used for compact information such as:
#   @
#   P2 08:42
# ============================================================

FONT_3X5 = {

    "A": [
        "010",
        "101",
        "111",
        "101",
        "101",
    ],

    "B": [
        "110",
        "101",
        "110",
        "101",
        "110",
    ],

    "C": [
        "011",
        "100",
        "100",
        "100",
        "011",
    ],

    "D": [
        "110",
        "101",
        "101",
        "101",
        "110",
    ],

    "E": [
        "111",
        "100",
        "110",
        "100",
        "111",
    ],

    "F": [
        "111",
        "100",
        "110",
        "100",
        "100",
    ],

    "G": [
        "011",
        "100",
        "101",
        "101",
        "011",
    ],

    "H": [
        "101",
        "101",
        "111",
        "101",
        "101",
    ],

    "I": [
        "111",
        "010",
        "010",
        "010",
        "111",
    ],

    "J": [
        "001",
        "001",
        "001",
        "101",
        "010",
    ],

    "K": [
        "101",
        "110",
        "100",
        "110",
        "101",
    ],

    "L": [
        "100",
        "100",
        "100",
        "100",
        "111",
    ],

    "M": [
        "10001",
        "11011",
        "10101",
        "10001",
        "10001",
    ],

    "N": [
        "101",
        "111",
        "111",
        "111",
        "101",
    ],

    "O": [
        "010",
        "101",
        "101",
        "101",
        "010",
    ],

    "P": [
        "110",
        "101",
        "110",
        "100",
        "100",
    ],

    "Q": [
        "010",
        "101",
        "101",
        "011",
        "001",
    ],

    "R": [
        "110",
        "101",
        "110",
        "101",
        "101",
    ],

    "S": [
        "011",
        "100",
        "010",
        "001",
        "110",
    ],

    "T": [
        "111",
        "010",
        "010",
        "010",
        "010",
    ],

    "U": [
        "101",
        "101",
        "101",
        "101",
        "010",
    ],

    "V": [
        "101",
        "101",
        "101",
        "010",
        "010",
    ],

    "W": [
        "101",
        "101",
        "101",
        "111",
        "101",
    ],

    "X": [
        "101",
        "101",
        "010",
        "101",
        "101",
    ],

    "Y": [
        "101",
        "101",
        "010",
        "010",
        "010",
    ],

    "Z": [
        "111",
        "001",
        "010",
        "100",
        "111",
    ],

    "0": [
        "010",
        "101",
        "111",
        "101",
        "010",
    ],

    "1": [
        "010",
        "110",
        "010",
        "010",
        "111",
    ],

    "2": [
        "110",
        "001",
        "010",
        "100",
        "111",
    ],

    "3": [
        "110",
        "001",
        "010",
        "001",
        "110",
    ],

    "4": [
        "101",
        "101",
        "111",
        "001",
        "001",
    ],

    "5": [
        "111",
        "100",
        "110",
        "001",
        "110",
    ],

    "6": [
        "011",
        "100",
        "110",
        "101",
        "010",
    ],

    "7": [
        "111",
        "001",
        "010",
        "010",
        "010",
    ],

    "8": [
        "010",
        "101",
        "010",
        "101",
        "010",
    ],

    "9": [
        "010",
        "101",
        "011",
        "001",
        "110",
    ],

    " ": [
        "000",
        "000",
        "000",
        "000",
        "000",
    ],

    "-": [
        "000",
        "000",
        "111",
        "000",
        "000",
    ],

    ":": [
        "000",
        "010",
        "000",
        "010",
        "000",
    ],

    ".": [
        "000",
        "000",
        "000",
        "000",
        "010",
    ],

    "@": [
        "010",
        "101",
        "111",
        "100",
        "011",
    ],

    "/": [
        "001",
        "001",
        "010",
        "100",
        "100",
    ],

    "!": [
        "010",
        "010",
        "010",
        "000",
        "010",
    ],
}


# ============================================================
# PIXEL BUFFER
# ============================================================

def new_frame():
    """Create a blank 64x32 RGB frame."""
    return [
        [BLACK for _ in range(WIDTH)]
        for _ in range(HEIGHT)
    ]


def set_pixel(frame, x, y, color):
    """Safely set one pixel."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        frame[y][x] = color


# ============================================================
# TEXT FUNCTIONS
# ============================================================

def text_width(text, font=FONT_5X7, spacing=1):
    """Return the width of a string in pixels."""
    width = 0

    for char in text.upper():
        glyph = font.get(char, font.get(" "))
        width += len(glyph[0]) + spacing

    if text:
        width -= spacing

    return width


def draw_text(frame, x, y, text, color=WHITE, font=FONT_5X7, spacing=1):
    """Draw text at x/y."""
    cursor_x = x

    for char in text.upper():

        glyph = font.get(char, font.get(" "))

        for row, line in enumerate(glyph):
            for col, pixel in enumerate(line):

                if pixel == "1":
                    set_pixel(
                        frame,
                        cursor_x + col,
                        y + row,
                        color
                    )

        cursor_x += len(glyph[0]) + spacing


def draw_text_center(
    frame,
    y,
    text,
    color=WHITE,
    font=FONT_5X7,
    spacing=1
):
    """Draw text horizontally centered."""
    width = text_width(text, font, spacing)
    x = (WIDTH - width) // 2
    draw_text(frame, x, y, text, color, font, spacing)


def fit_text(text, max_width, font=FONT_5X7, spacing=1):
    """
    Return the longest version of text that fits.

    If necessary, progressively abbreviate long names.
    """

    text = text.upper()

    if text_width(text, font, spacing) <= max_width:
        return text

    # Try initials + last name.
    parts = text.split()

    if len(parts) >= 2:

        abbreviated = []

        for part in parts[:-1]:
            if part:
                abbreviated.append(part[0] + ".")

        abbreviated.append(parts[-1])

        candidate = " ".join(abbreviated)

        if text_width(candidate, font, spacing) <= max_width:
            return candidate

        text = candidate

    # Hard truncate if still too long.
    result = ""

    for char in text:
        candidate = result + char

        if text_width(candidate, font, spacing) <= max_width:
            result = candidate
        else:
            break

    return result.rstrip()


# ============================================================
# TEAM COLOR
# ============================================================

def get_team_color(team, league=None):

    if league == "PWHL":
        key = f"{team}_PWHL"

        if key in TEAM_COLORS:
            return TEAM_COLORS[key]

    return TEAM_COLORS.get(team, WHITE)


# ============================================================
# LEAGUE HEADER
# ============================================================

def draw_league(frame, league):
    draw_text_center(
        frame,
        1,
        league,
        WHITE,
        FONT_3X5
    )


# ============================================================
# PREGAME
# ============================================================

def render_pregame(game):

    frame = new_frame()

    league = game.get("league", "")
    away = game.get("away", "")
    home = game.get("home", "")
    start_time = game.get("start_time")

    draw_league(frame, league)

    # --------------------------------------------------------
    # Team colors
    # --------------------------------------------------------

    away_color = get_team_color(away, league)
    home_color = get_team_color(home, league)

    # --------------------------------------------------------
    # Team positions
    #
    # Left team occupies roughly x=2..25
    # Right team occupies roughly x=39..62
    # --------------------------------------------------------

    away_width = text_width(
        away,
        FONT_5X7
    )

    home_width = text_width(
        home,
        FONT_5X7
    )

    away_x = (27 - away_width) // 2
    home_x = 37 + ((27 - home_width) // 2)

    draw_text(
        frame,
        away_x,
        13,
        away,
        away_color
    )

    # --------------------------------------------------------
    # @
    # --------------------------------------------------------

    draw_text(
        frame,
        31,
        14,
        "@",
        WHITE,
        FONT_3X5
    )

    # --------------------------------------------------------
    # Home team
    # --------------------------------------------------------

    draw_text(
        frame,
        home_x,
        13,
        home,
        home_color
    )

    # --------------------------------------------------------
    # Start time
    # --------------------------------------------------------

    if start_time:
        time_text = str(start_time)
    else:
        time_text = "TBD"

    draw_text_center(
        frame,
        25,
        time_text,
        WHITE,
        FONT_3X5
    )

    return frame


# ============================================================
# LIVE
# ============================================================

def render_live(game):

    frame = new_frame()

    league = game.get("league", "")
    away = game.get("away", "")
    home = game.get("home", "")

    away_score = game.get("away_score", 0)
    home_score = game.get("home_score", 0)

    period = game.get("period")
    clock = game.get("clock")

    draw_league(frame, league)

    # --------------------------------------------------------
    # Teams
    # --------------------------------------------------------

    away_color = get_team_color(away, league)
    home_color = get_team_color(home, league)

    draw_text(
        frame,
        2,
        13,
        away,
        away_color
    )

    score_text = f"{away_score} - {home_score}"

    draw_text_center(
        frame,
        13,
        score_text,
        WHITE
    )

    draw_text(
        frame,
        54,
        13,
        home,
        home_color
    )

    # --------------------------------------------------------
    # Period / clock
    # --------------------------------------------------------

    if period is not None and clock:

        status = f"P{period} {clock}"

        draw_text_center(
            frame,
            23,
            status,
            WHITE,
            FONT_3X5
        )

    return frame


# ============================================================
# FINAL
# ============================================================

def render_final(game):

    frame = new_frame()

    league = game.get("league", "")
    away = game.get("away", "")
    home = game.get("home", "")

    away_score = game.get("away_score", 0)
    home_score = game.get("home_score", 0)

    draw_text_center(
        frame,
        1,
        f"{league} FINAL",
        WHITE,
        FONT_3X5
    )

    away_color = get_team_color(away, league)
    home_color = get_team_color(home, league)

    draw_text(
        frame,
        2,
        14,
        away,
        away_color
    )

    draw_text_center(
        frame,
        14,
        f"{away_score} - {home_score}",
        WHITE
    )

    draw_text(
        frame,
        54,
        14,
        home,
        home_color
    )

    return frame


# ============================================================
# GOAL ALERT
# ============================================================

def render_goal(game, goal):

    frame = new_frame()

    league = game.get("league", "")

    scoring_team = goal.get(
        "team",
        ""
    )

    scorer = goal.get(
        "scorer",
        ""
    )

    assists = goal.get(
        "assists",
        []
    )

    period = goal.get(
        "period"
    )

    clock = goal.get(
        "time"
    )

    # --------------------------------------------------------
    # GOAL!
    # --------------------------------------------------------

    draw_text_center(
        frame,
        1,
        "GOAL!",
        YELLOW
    )

    # --------------------------------------------------------
    # Scoring team
    # --------------------------------------------------------

    team_color = get_team_color(
        scoring_team,
        league
    )

    draw_text_center(
        frame,
        9,
        scoring_team,
        team_color
    )

    # --------------------------------------------------------
    # Scorer
    # --------------------------------------------------------

    scorer_text = fit_text(
        scorer,
        58
    )

    draw_text_center(
        frame,
        14,
        scorer_text,
        WHITE
    )

    # --------------------------------------------------------
    # Assists
    # --------------------------------------------------------

    if assists:

        assist_text = " / ".join(
            fit_text(
                assist,
                20
            )
            for assist in assists
        )

        assist_text = fit_text(
            assist_text,
            62,
            FONT_3X5
        )

        draw_text_center(
            frame,
            21,
            assist_text,
            WHITE,
            FONT_3X5
        )

    # --------------------------------------------------------
    # Period / time
    # --------------------------------------------------------

    if period is not None and clock:

        status = f"P{period} {clock}"

        draw_text_center(
            frame,
            27,
            status,
            WHITE,
            FONT_3X5
        )

    return frame


# ============================================================
# NO GAMES
# ============================================================

def render_no_games():

    frame = new_frame()

    draw_text_center(
        frame,
        13,
        "NO GAMES",
        WHITE
    )

    return frame


# ============================================================
# GENERIC GAME RENDERER
# ============================================================

def render_game(game):

    status = game.get(
        "status",
        "PREGAME"
    )

    if status == "LIVE":
        return render_live(game)

    if status == "FINAL":
        return render_final(game)

    return render_pregame(game)