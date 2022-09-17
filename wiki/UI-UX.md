# Routes

## Main page

Displayed only for unauthorized users.

* title
* player's nickname input
* "begin" button

## Leaderboard

HTML representation of [player](Database.md#player)'s database table.

# Protected routes

## Game page

Consists of following components:

* game title + player count
* game status + nickname
* two [gameboards](#gameboard)
* ready button

---

### Gameboard

Single interactive gameboard, written in HTML's [canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API), capable of:

* emiting websocket events
* ship rearrangement