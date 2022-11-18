from models import Orientation, Warship
from itertools import cycle

warship_pool = cycle([
    [
        Warship(x=0, y=5, length=2, orientation=Orientation.VERTICAL),
        Warship(x=0, y=0, length=1, orientation=Orientation.VERTICAL),
        Warship(x=2, y=2, length=2, orientation=Orientation.HORIZONTAL),
        Warship(x=0, y=3, length=1, orientation=Orientation.VERTICAL),
        Warship(x=7, y=3, length=3, orientation=Orientation.HORIZONTAL),
        Warship(x=4, y=6, length=3, orientation=Orientation.VERTICAL),
        Warship(x=9, y=5, length=1, orientation=Orientation.VERTICAL),
        Warship(x=6, y=6, length=4, orientation=Orientation.VERTICAL),
        Warship(x=0, y=8, length=2, orientation=Orientation.HORIZONTAL),
        Warship(x=4, y=9, length=1, orientation=Orientation.VERTICAL)
    ],
    [
        Warship(x=0, y=4, length=1, orientation=Orientation.VERTICAL),
        Warship(x=1, y=9, length=1, orientation=Orientation.VERTICAL),
        Warship(x=0, y=6, length=2, orientation=Orientation.VERTICAL),
        Warship(x=2, y=2, length=2, orientation=Orientation.VERTICAL),
        Warship(x=0, y=3, length=3, orientation=Orientation.VERTICAL),
        Warship(x=4, y=4, length=3, orientation=Orientation.HORIZONTAL),
        Warship(x=8, y=4, length=1, orientation=Orientation.VERTICAL),
        Warship(x=5, y=6, length=4, orientation=Orientation.VERTICAL),
        Warship(x=0, y=7, length=1, orientation=Orientation.VERTICAL),
        Warship(x=0, y=9, length=2, orientation=Orientation.HORIZONTAL)
    ]
])
