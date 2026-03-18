'''Data models for the Elements multiplayer game server'''

from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class PlayerStatus(str, Enum):
    '''Player connection status'''
    IDLE = "idle"
    IN_ROOM = "in_room"
    PLAYING = "playing"


class Player(BaseModel):
    '''Represents a connected player'''
    id: str
    name: str
    status: PlayerStatus = PlayerStatus.IDLE


class Room(BaseModel):
    '''Represents a game room'''
    id: str
    name: str
    max_players: int = 4
    players: set[str] = set()


class GameMessage(BaseModel):
    '''Message exchanged between players via WebSocket'''
    type: str
    data: Optional[dict[str, Any]] = None
    player_id: Optional[str] = None
