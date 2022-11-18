from passlib.context import CryptContext
import jwt
from datetime import timezone, datetime, timedelta
from starlette.authentication import AuthenticationBackend, AuthenticationError
from crud import get_player
from database import get_db
from models import Player

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
        raise AuthenticationError()


def get_current_player(token: str) -> Player | None:
    """
    Finds currently authenticated player.
    """
    player_id: str = decode_token(token)
    with next(get_db()) as db:
        player = get_player(db, player_id)
        if player:
            return player

        raise AuthenticationError()


class WebSocketAuthBackend(AuthenticationBackend):
    """
    WebSocket authentication middleware.
    """
    async def authenticate(self, conn):
        token = conn.query_params.get("token")

        if not token:
            raise AuthenticationError()

        player = get_current_player(token)
        conn.state.player = player
