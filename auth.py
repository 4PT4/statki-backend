from database import get_db
from models import Player
from passlib.context import CryptContext
import jwt
from datetime import timezone, datetime, timedelta
from starlette.authentication import AuthenticationBackend, AuthenticationError
from schemas import PlayerInternal

SECRET_KEY = "f170e0d954edfcfb3e63759e934fd220580ab333b58c6d14f3762a02423c198f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies password hashes.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes password.
    """
    return pwd_context.hash(password)


def get_player(id: int) -> PlayerInternal:
    """
    Gets player by id.
    """
    with next(get_db()) as db:
        query = db.query(Player)
        query = query.filter(Player.id == id)
        player: Player = query.first()

        if player:
            return PlayerInternal(
                id=player.id,
                nickname=player.nickname,
                wins=player.wins,
                loses=player.loses,
                winStreak=player.win_streak,
                lastSeen=player.last_seen,
                warships=player.warships
            )

    raise AuthException("Player doesn't exist.")


def create_token(player_id: str) -> str:
    """
    Creates JWT.
    """
    current_timestamp = datetime.now(tz=timezone.utc)
    time_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": player_id,
        "iat": current_timestamp,
        "exp": current_timestamp + time_delta
    }
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

    return token


def decode_token(token: str) -> str:
    """
    Decodes JWT.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id = decoded["sub"]
        return id
    except jwt.PyJWTError:
        raise AuthException("Couldn't decode access token.")


async def get_current_player(token: str) -> PlayerInternal:
    """
    Finds currently authenticated player.
    """
    player_id: str = decode_token(token)
    player: PlayerInternal = get_player(player_id)

    return player


class WebSocketAuthBackend(AuthenticationBackend):
    """
    WebSocket authentication middleware.
    """
    async def authenticate(self, conn):
        token = conn.query_params.get("token")

        try:
            if not token:
                raise AuthException("No token provided.")

            player = await get_current_player(token)
            conn.state.player = player
        except AuthException:
            raise AuthenticationError()


class AuthException(Exception):
    def __init__(self, message) -> None:
        self.message = message
