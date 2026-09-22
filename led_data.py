# ============================================================
# led_data.py
# Hockey data layer for the Raspberry Pi LED scoreboard
# ============================================================

import os
import requests

from datetime import datetime
from zoneinfo import ZoneInfo


# ============================================================
# CONFIGURATION
# ============================================================

EST = ZoneInfo("America/New_York")

NHL_SCOREBOARD_URL = (
    "https://api-web.nhle.com/v1/scoreboard/now"
)

PWHL_SCHEDULE_URL = (
    "https://lscluster.hockeytech.com/feed/"
    "index.php"
    "?feed=modulekit"
    "&view=schedule"
    "&key=446521baf8c38984"
    "&fmt=json"
    "&client_code=pwhl"
    "&lang=en"
    "&league_code=pwhl"
)

PWHL_PBP_URL = (
    "https://lscluster.hockeytech.com/feed/"
    "index.php"
    "?feed=gc"
    "&tab=pxpverbose"
    "&game_id={}"
    "&key=446521baf8c38984"
    "&client_code=pwhl"
)


# ============================================================
# REQUEST SESSION
# ============================================================

session = requests.Session()

if os.name == "nt":
    # Windows
    import certifi
    session.verify = certifi.where()
else:
    # Linux / Raspberry Pi
    system_ca = "/etc/ssl/certs/ca-certificates.crt"

    if os.path.exists(system_ca):
        session.verify = system_ca


# ============================================================
# CACHES
# ============================================================

# Last known combined score for each game.

_score_cache = {}


# Most recent known goal for each game.

_goal_cache = {}


# ============================================================
# NHL
# ============================================================

def get_nhl_games():
    """
    Retrieve today's NHL games.

    Play-by-play is only requested when a live game's
    score changes.
    """

    try:

        response = session.get(
            NHL_SCOREBOARD_URL,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        print(
            f"NHL API error: {e}"
        )

        return []


    today = datetime.now(
        EST
    ).date()


    games = []


    # ========================================================
    # TODAY
    # ========================================================

    for day in data.get(
        "gamesByDate",
        []
    ):

        try:

            game_date = datetime.strptime(
                day["date"],
                "%Y-%m-%d"
            ).date()

        except (
            KeyError,
            ValueError
        ):

            continue


        if game_date != today:

            continue


        # ====================================================
        # GAMES
        # ====================================================

        for game in day.get(
            "games",
            []
        ):

            game_data = build_nhl_game(
                game
            )


            if game_data:

                games.append(
                    game_data
                )


    return games


# ============================================================
# BUILD NHL GAME
# ============================================================

def build_nhl_game(game):
    """
    Convert an NHL API game into our normalized format.
    """

    away_team = game[
        "awayTeam"
    ]["abbrev"]

    home_team = game[
        "homeTeam"
    ]["abbrev"]


    away_score = game[
        "awayTeam"
    ].get(
        "score",
        0
    )

    home_score = game[
        "homeTeam"
    ].get(
        "score",
        0
    )


    game_state = game.get(
        "gameState",
        ""
    )


    game_id = game[
        "id"
    ]


    # ========================================================
    # BASE OBJECT
    # ========================================================

    game_data = {

        "league": "NHL",

        "game_id": game_id,

        "away": away_team,

        "home": home_team,

        "away_score": away_score,

        "home_score": home_score,

        "status": None,

        "period": None,

        "clock": None,

        "start_time": None,

        "latest_goal": _goal_cache.get(
            game_id
        )
    }


    # ========================================================
    # PREGAME
    # ========================================================

    if game_state == "FUT":

        game_data[
            "status"
        ] = "PREGAME"


        utc_time = game.get(
            "startTimeUTC"
        )


        if utc_time:

            try:

                utc_dt = datetime.fromisoformat(
                    utc_time.replace(
                        "Z",
                        "+00:00"
                    )
                )

                est_dt = utc_dt.astimezone(
                    EST
                )

                game_data[
                    "start_time"
                ] = est_dt.strftime(
                    "%I:%M %p"
                ).lstrip("0")

            except ValueError:

                pass


        # No PBP needed.

        return game_data


    # ========================================================
    # FINAL
    # ========================================================

    if game_state == "OFF":

        game_data[
            "status"
        ] = "FINAL"


        # No PBP needed.

        return game_data


    # ========================================================
    # LIVE
    # ========================================================

    game_data[
        "status"
    ] = "LIVE"


    period_descriptor = game.get(
        "periodDescriptor",
        {}
    )


    game_data[
        "period"
    ] = period_descriptor.get(
        "number"
    )


    game_data[
        "clock"
    ] = game.get(
        "clock",
        {}
    ).get(
        "timeRemaining"
    )


    # ========================================================
    # SCORE CHANGE DETECTION
    # ========================================================

    current_score = (
        away_score,
        home_score
    )


    previous_score = _score_cache.get(
        game_id
    )


    # First time seeing this live game.

    if previous_score is None:

        _score_cache[
            game_id
        ] = current_score


        # Get the existing latest goal once.

        latest_goal = get_latest_nhl_goal(
            game
        )


        if latest_goal:

            _goal_cache[
                game_id
            ] = latest_goal

            game_data[
                "latest_goal"
            ] = latest_goal


        return game_data


    # ========================================================
    # SCORE CHANGED
    # ========================================================

    if current_score != previous_score:

        _score_cache[
            game_id
        ] = current_score


        latest_goal = get_latest_nhl_goal(
            game
        )


        if latest_goal:

            _goal_cache[
                game_id
            ] = latest_goal

            game_data[
                "latest_goal"
            ] = latest_goal


    else:

        # Score hasn't changed.
        # Use cached goal information.

        game_data[
            "latest_goal"
        ] = _goal_cache.get(
            game_id
        )


    return game_data


# ============================================================
# NHL LATEST GOAL
# ============================================================

def get_latest_nhl_goal(game):
    """
    Retrieve the most recent NHL goal from play-by-play.
    """

    game_id = game[
        "id"
    ]


    url = (
        "https://api-web.nhle.com/v1/"
        f"gamecenter/{game_id}/play-by-play"
    )


    try:

        response = session.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        print(
            f"NHL play-by-play error "
            f"({game_id}): {e}"
        )

        return None


    # ========================================================
    # PLAYER LOOKUP
    # ========================================================

    player_lookup = {}


    for player in data.get(
        "rosterSpots",
        []
    ):

        try:

            player_id = str(
                player["playerId"]
            )

            first_name = (
                player["firstName"]["default"]
            )

            last_name = (
                player["lastName"]["default"]
            )

            player_lookup[
                player_id
            ] = (
                f"{first_name} {last_name}"
            )

        except (
            KeyError,
            TypeError
        ):

            continue


    # ========================================================
    # GOALS
    # ========================================================

    goals = []


    for play in data.get(
        "plays",
        []
    ):

        if play.get(
            "typeCode"
        ) != 505:

            continue


        details = play.get(
            "details",
            {}
        )


        scorer_id = details.get(
            "scoringPlayerId"
        )

        assist1_id = details.get(
            "assist1PlayerId"
        )

        assist2_id = details.get(
            "assist2PlayerId"
        )


        # =====================================================
        # TEAM
        # =====================================================

        team_id = details.get(
            "eventOwnerTeamId"
        )


        if team_id == game[
            "awayTeam"
        ]["id"]:

            goal_team = game[
                "awayTeam"
            ]["abbrev"]

        elif team_id == game[
            "homeTeam"
        ]["id"]:

            goal_team = game[
                "homeTeam"
            ]["abbrev"]

        else:

            goal_team = "UNK"


        # =====================================================
        # ASSISTS
        # =====================================================

        assists = []


        if assist1_id:

            name = player_lookup.get(
                str(assist1_id)
            )

            if name:

                assists.append(
                    name
                )


        if assist2_id:

            name = player_lookup.get(
                str(assist2_id)
            )

            if name:

                assists.append(
                    name
                )


        # =====================================================
        # PERIOD / TIME
        # =====================================================

        period = (
            play.get(
                "periodDescriptor",
                {}
            ).get(
                "number"
            )
        )


        time = play.get(
            "timeInPeriod"
        )


        goals.append({

            "goal_id": play.get(
                "eventId"
            ),

            "team": goal_team,

            "scorer": player_lookup.get(
                str(scorer_id),
                "Unknown"
            ),

            "assists": assists,

            "period": period,

            "time": time
        })


    if not goals:

        return None


    return goals[-1]


# ============================================================
# PWHL
# ============================================================

def get_pwhl_games():
    """
    Retrieve today's PWHL games.

    Play-by-play is only requested when a live game's
    score changes.
    """

    try:

        response = session.get(
            PWHL_SCHEDULE_URL,
            timeout=10
        )

        response.raise_for_status()

        schedule_data = response.json()

    except Exception as e:

        print(
            f"PWHL API error: {e}"
        )

        return []


    games = (
        schedule_data
        .get("SiteKit", {})
        .get("Schedule", [])
    )


    today = datetime.now(
        EST
    ).strftime(
        "%Y-%m-%d"
    )


    normalized_games = []


    for game in games:

        if game.get(
            "date_played",
            ""
        ) != today:

            continue


        game_data = build_pwhl_game(
            game
        )


        if game_data:

            normalized_games.append(
                game_data
            )


    return normalized_games


# ============================================================
# BUILD PWHL GAME
# ============================================================

def build_pwhl_game(game):
    """
    Convert a PWHL API game into our normalized format.
    """

    game_id = game[
        "game_id"
    ]


    away_team = game[
        "visiting_team_code"
    ]

    home_team = game[
        "home_team_code"
    ]


    try:

        away_score = int(
            game.get(
                "visiting_goal_count",
                0
            )
        )

    except (
        ValueError,
        TypeError
    ):

        away_score = 0


    try:

        home_score = int(
            game.get(
                "home_goal_count",
                0
            )
        )

    except (
        ValueError,
        TypeError
    ):

        home_score = 0


    game_status = game.get(
        "game_status",
        ""
    )


    # ========================================================
    # STATUS
    # ========================================================

    if "Final" in game_status:

        status = "FINAL"

    elif game.get(
        "started"
    ) == "1":

        status = "LIVE"

    else:

        status = "PREGAME"


    game_data = {

        "league": "PWHL",

        "game_id": game_id,

        "away": away_team,

        "home": home_team,

        "away_score": away_score,

        "home_score": home_score,

        "status": status,

        "period": None,

        "clock": None,

        "start_time": None,

        "latest_goal": _goal_cache.get(
            game_id
        )
    }


    # ========================================================
    # PREGAME
    # ========================================================

    if status == "PREGAME":

        game_data[
            "start_time"
        ] = extract_pwhl_start_time(
            game
        )


        return game_data


    # ========================================================
    # FINAL
    # ========================================================

    if status == "FINAL":

        return game_data


    # ========================================================
    # LIVE
    # ========================================================

    current_score = (
        away_score,
        home_score
    )


    previous_score = _score_cache.get(
        game_id
    )


    # ========================================================
    # FIRST LIVE OBSERVATION
    # ========================================================

    if previous_score is None:

        _score_cache[
            game_id
        ] = current_score


        latest_goal = get_latest_pwhl_goal(
            game_id
        )


        if latest_goal:

            _goal_cache[
                game_id
            ] = latest_goal

            game_data[
                "latest_goal"
            ] = latest_goal


        return game_data


    # ========================================================
    # SCORE CHANGED
    # ========================================================

    if current_score != previous_score:

        _score_cache[
            game_id
        ] = current_score


        latest_goal = get_latest_pwhl_goal(
            game_id
        )


        if latest_goal:

            _goal_cache[
                game_id
            ] = latest_goal

            game_data[
                "latest_goal"
            ] = latest_goal


    else:

        game_data[
            "latest_goal"
        ] = _goal_cache.get(
            game_id
        )


    return game_data


# ============================================================
# PWHL START TIME
# ============================================================

def extract_pwhl_start_time(game):
    """
    Extract a display-friendly PWHL start time.
    """

    possible_fields = [

        "game_time",

        "start_time",

        "scheduled_time",

        "time"
    ]


    for field in possible_fields:

        value = game.get(
            field
        )


        if value:

            return str(
                value
            )


    return None


# ============================================================
# PWHL LATEST GOAL
# ============================================================

def get_latest_pwhl_goal(game_id):
    """
    Retrieve the most recent PWHL goal.
    """

    url = PWHL_PBP_URL.format(
        game_id
    )


    try:

        response = session.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        print(
            f"PWHL play-by-play error "
            f"({game_id}): {e}"
        )

        return None


    plays = (
        data
        .get("GC", {})
        .get("Pxpverbose", [])
    )


    goals = []


    PWHL_TEAM_IDS = {

        "1": "BOS",
        "2": "MIN",
        "3": "MTL",
        "4": "NY",
        "5": "OTT",
        "6": "TOR"
    }


    for play in plays:

        if play.get(
            "event"
        ) != "goal":

            continue


        scorer = play.get(
            "goal_scorer"
        )


        if not scorer:

            continue


        assist1 = play.get(
            "assist1_player"
        )

        assist2 = play.get(
            "assist2_player"
        )


        assists = []


        if assist1:

            assists.append(
                f"{assist1['first_name']} "
                f"{assist1['last_name']}"
            )


        if assist2:

            assists.append(
                f"{assist2['first_name']} "
                f"{assist2['last_name']}"
            )


        team_id = str(
            play.get(
                "team_id",
                ""
            )
        )


        goal_team = (
            PWHL_TEAM_IDS.get(
                team_id,
                "UNK"
            )
        )


        goals.append({

            "goal_id": play.get(
                "id"
            ),

            "team": goal_team,

            "scorer": (
                f"{scorer['first_name']} "
                f"{scorer['last_name']}"
            ),

            "assists": assists,

            "period": play.get(
                "period"
            ),

            "time": play.get(
                "time"
            )
        })


    if not goals:

        return None


    return goals[-1]


# ============================================================
# ALL GAMES
# ============================================================

def get_all_games():
    """
    Retrieve today's NHL + PWHL games.
    """

    games = []


    games.extend(
        get_nhl_games()
    )


    games.extend(
        get_pwhl_games()
    )


    return games


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    games = get_all_games()


    print()

    print(
        "=" * 60
    )

    print(
        "LED DATA TEST"
    )

    print(
        "=" * 60
    )


    if not games:

        print(
            "No games found today."
        )


    else:

        for game in games:

            print()

            print(
                f"{game['league']} | "
                f"{game['away']} @ "
                f"{game['home']}"
            )

            print(
                f"Status: "
                f"{game['status']}"
            )

            print(
                f"Score: "
                f"{game['away_score']} - "
                f"{game['home_score']}"
            )


            if game[
                "start_time"
            ]:

                print(
                    f"Start: "
                    f"{game['start_time']}"
                )


            if game[
                "latest_goal"
            ]:

                goal = game[
                    "latest_goal"
                ]


                print(
                    f"Latest goal: "
                    f"{goal['team']} - "
                    f"{goal['scorer']}"
                )


                if goal[
                    "assists"
                ]:

                    print(
                        "Assists: "
                        + ", ".join(
                            goal["assists"]
                        )
                    )


                print(
                    f"Time: "
                    f"P{goal['period']} "
                    f"{goal['time']}"
                )