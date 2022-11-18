# Overview

When a player gets ready he is placed in the game queue. If there is more than one player in the queue, a new game session is created.

Players are being connected, the oponent is known, it's time to re-render second gameboard. The game begins, session waits for shots from randomly selected player. Current turn has to be tracked by the server.

After all the warships were shot game ends with proper [exit code](#gameexitcode) for each player.

## GameExitCode

> see [enums in python](https://docs.python.org/3/library/enum.html)

* WIN
* LOSE
* ENEMY_DISCONNECTED