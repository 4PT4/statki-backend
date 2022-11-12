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
