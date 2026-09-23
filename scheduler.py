from datetime import datetime
from zoneinfo import ZoneInfo


EST = ZoneInfo("America/New_York")


def get_display_mode(now=None):
    """
    Determine what the LED scoreboard should be displaying.

    Returns one of:
        "OFF"
        "MORNING_RESULTS"
        "LIVE"

    Schedule:

    Monday-Friday:
        01:00-06:00  OFF
        06:00-07:00  Previous night's final scores
        07:00-16:00  OFF
        16:00-01:00  Today's games

    Saturday-Sunday:
        01:00-08:00  OFF
        08:00-01:00  Today's games
    """

    if now is None:
        now = datetime.now(EST)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=EST)
    else:
        now = now.astimezone(EST)

    weekday = now.weekday()  # Monday=0 ... Sunday=6
    hour = now.hour

    # -----------------------------------------
    # Monday-Friday
    # -----------------------------------------
    if weekday < 5:

        # 6:00 AM - 7:00 AM
        if hour == 6:
            return "MORNING_RESULTS"

        # 4:00 PM - midnight
        if hour >= 16:
            return "LIVE"

        # Midnight - 1:00 AM
        # Note: hour == 0 is still part of the previous
        # evening's operating period.
        if hour == 0:
            return "LIVE"

        return "OFF"

    # -----------------------------------------
    # Saturday-Sunday
    # -----------------------------------------
    else:

        # 8:00 AM - midnight
        if hour >= 8:
            return "LIVE"

        # Midnight - 1:00 AM
        if hour == 0:
            return "LIVE"

        return "OFF"


def is_display_on(now=None):
    return get_display_mode(now) != "OFF"


if __name__ == "__main__":
    print("Current time:", datetime.now(EST).strftime("%Y-%m-%d %I:%M:%S %p %Z"))
    print("Display mode:", get_display_mode())
