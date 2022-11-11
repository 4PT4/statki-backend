from database import get_db
from sqlalchemy.orm import Session
from models import Player
from passlib.context import CryptContext
import jwt
from datetime import timezone, datetime
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)

SECRET_KEY = "f170e0d954edfcfb3e63759e934fd220580ab333b58c6d14f3762a02423c198f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_player(db: Session, id: int) -> Player:
    query = db.query(Player)
    query = query.filter(Player.id == id)
    player: Player = query.first()

    return player


def create_token(player_id: str) -> str:
    data = {
        "sub": player_id,
        "iat": datetime.now(tz=timezone.utc)
    }
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return token


def decode_token(token: str):
    decoded = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    id = decoded["sub"]
    print(id)
    return id


async def get_current_player(db: Session, token: str) -> Player:
    player_id: str = decode_token(token)
    player: Player = get_player(db, player_id)

    return player


class WebSocketAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        token = conn.query_params.get("token")

        if not token:
            raise AuthenticationError("No token provided.")
        
        with next(get_db()) as db:
            player = await get_current_player(db, token)
            conn.state.player = player
            if not player:
                raise AuthenticationError("Invalid token.")

        return AuthCredentials(), SimpleUser(player.nickname)
