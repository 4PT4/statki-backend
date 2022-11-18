import time
import math
import uuid

def get_current_timestamp():
    """
    Returns current timestamp rounded down.
    """
    return math.floor(time.time())


def get_uuid():
    """
    Returns UUID string.
    """
    return str(uuid.uuid4())


def create_player_payload(player):
    """
    Creates payload for "start" message.
    """
    win_rate = 0
    try:
        win_rate = player.wins / (player.wins + player.loses) * 100
        win_rate = round(win_rate)
    except ZeroDivisionError:
        pass

    return {"nickname": player.nickname, "winRate": win_rate}


def create_init_payload(player):
    """
    Creates payload for "init" message.
    """
    return {"warships": player.warships, "nickname": player.nickname}
