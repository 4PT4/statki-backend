from sqlalchemy.orm import Session, joinedload
import schemas
import models
import auth
import models
import predefined_data

def create_player(db: Session, credentials: schemas.Credentials) -> str:
    """
    Creates new player. Returns id.
    """
    player = models.Player(
        nickname=credentials.nickname,
        password=auth.get_password_hash(credentials.password),
        warships=next(predefined_data.warship_pool)
    )
    db.add(player)
    db.commit()
    db.refresh(player)

    return player.id


def get_player(db: Session, id: str) -> models.Player:
    """
    Gets player by id.
    """
    query = db.query(models.Player)
    query = query.filter(models.Player.id == id)
    query = query.options(joinedload(models.Player.warships))
    player: models.Player = query.first()

    if not player:
        return

    return player
