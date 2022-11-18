from models import Orientation, Warship
from itertools import cycle

warship_pool = cycle([
    [
        Warship(x=2, y=0, length=3, orientation=Orientation.HORIZONTAL),
        Warship(x=7, y=1, length=1, orientation=Orientation.HORIZONTAL),
        Warship(x=9, y=1, length=2, orientation=Orientation.VERTICAL),
        Warship(x=1, y=3, length=4, orientation=Orientation.HORIZONTAL),
        Warship(x=0, y=5, length=2, orientation=Orientation.VERTICAL),
        Warship(x=8, y=5, length=1, orientation=Orientation.HORIZONTAL),
        Warship(x=2, y=6, length=3, orientation=Orientation.HORIZONTAL),
        Warship(x=8, y=8, length=2, orientation=Orientation.VERTICAL),
        Warship(x=3, y=9, length=1, orientation=Orientation.HORIZONTAL),
        Warship(x=5, y=9, length=1, orientation=Orientation.HORIZONTAL)
    ],
    [
        Warship(x=3, y=0, length=1, orientation=Orientation.HORIZONTAL),
        Warship(x=0, y=2, length=1, orientation=Orientation.HORIZONTAL),
        Warship(x=8, y=2, length=2, orientation=Orientation.HORIZONTAL),
        Warship(x=2, y=3, length=3, orientation=Orientation.HORIZONTAL),
        Warship(x=9, y=4, length=1, orientation=Orientation.HORIZONTAL),
        Warship(x=3, y=5, length=4, orientation=Orientation.HORIZONTAL),
        Warship(x=0, y=6, length=3, orientation=Orientation.VERTICAL),
        Warship(x=8, y=6, length=2, orientation=Orientation.HORIZONTAL),
        Warship(x=5, y=7, length=1, orientation=Orientation.HORIZONTAL),
        Warship(x=2, y=8, length=2, orientation=Orientation.HORIZONTAL)
    ]
])
