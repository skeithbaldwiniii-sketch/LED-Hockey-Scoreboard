def process_goal_event(play):

    scorer = (
        play["goal_scorer"]
    )

    assist1 = (
        play.get(
            "assist1_player"
        )
    )

    assist2 = (
        play.get(
            "assist2_player"
        )
    )

    return {

        "team": scorer["team_code"],

        "scorer":
            f"{scorer['first_name']} "
            f"{scorer['last_name']}",

        "assist1":
            f"{assist1['first_name']} "
            f"{assist1['last_name']}"
            if assist1 else "None",

        "assist2":
            f"{assist2['first_name']} "
            f"{assist2['last_name']}"
            if assist2 else "None",

        "x":
            play["x_location"],

        "y":
            play["y_location"],

        "time":
            play["time"],

        "period":
            play["period"],

        "plus":
            play["plus"],

        "minus":
            play["minus"]
    }