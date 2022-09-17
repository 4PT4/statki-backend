# REST endpoints

<details>
 <summary><code>GET</code> <code><b>/players</b></code></summary>

##### Parameters

> |name|type|data type|description|
> |-|-|-|-|
> |last_seen|not required|int|shows only players seen before specified date|


##### Responses

> |http code|content-type|response|
> |-|-|-|
> |`200`|`application/json`|`{ "players": [] }`|

</details>

Retrieve player list. Paginated. Ordered by rating.

# Websocket events

## Client-emited

<details>
 <summary><code>fire</code></summary>

##### Payload

> |name|type|data type|description|
> |-|-|-|-|
> |x|required|int|N/A|
> |y|required|int|N/A|


##### Example response

```json
{ "hit": false }
```

</details>

Shoot enemy warship.

---

<details>
 <summary><code>ready</code></summary>

##### Payload

> |name|type|data type|description|
> |-|-|-|-|
> |ships|not required|array (JSON)|update player ships if they were rearranged|


##### Example response

```json
{ "queued": true }
```

</details>

Ready up.

## Server-emited

<details>
 <summary><code>started</code></summary>

##### Example payload

```json
{
    "nickname": "john",
    "win_rate": 0.89
}
```

</details>

Game has started.

---

<details>
 <summary><code>stopped</code></summary>

##### Example payload

```json
{
    "code": 0
}
```

see [game exit code](Mechanics.md#game-exit-code)

</details>

Game has stopped.

---

Additional event namespaces can be defined for `player` and `game` if needed.