# Development assumptions

## Documentation

Any required documentation is written within coded functionality using [docstring](https://peps.python.org/pep-0257/).

## Tests

Tests are written in python's [pytest](https://docs.pytest.org/en/7.1.x/) library.

In addition static code analysis is used, so **use [type hints](https://realpython.com/lessons/type-hinting/)**. Variable and function names have to be self-explanatory.

```
p = get_plrs() ❌
players = get_players() ✅
``` 

# Table of contents

* [UI/UX](UI-UX.md)
* [API](API.md)
* [Database](Database.md)
* [Game mechanics](Mechanics.md)