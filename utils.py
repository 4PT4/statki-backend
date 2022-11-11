import time
import math
import uuid


def get_current_timestamp():
    return math.floor(time.time())


def get_uuid():
    return str(uuid.uuid4())
