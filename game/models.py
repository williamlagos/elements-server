"""Data models for the Elements multiplayer game server"""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel


class PlayerStatus(StrEnum):
    """Player connection status"""

    IDLE = "idle"
    IN_ROOM = "in_room"
    PLAYING = "playing"


class Player(BaseModel):
    """Represents a connected player"""

    id: str
    name: str
    status: PlayerStatus = PlayerStatus.IDLE


class Room(BaseModel):
    """Represents a game room"""

    id: str
    name: str
    max_players: int = 4
    players: set[str] = set()


class GameMessage(BaseModel):
    """Message exchanged between players via WebSocket"""

    type: str
    data: dict[str, Any] | None = None
    player_id: str | None = None
