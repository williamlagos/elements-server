'''Elements Game Server – asyncio-powered multiplayer server'''

import uuid
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from game.manager import ConnectionManager
from game.models import GameMessage, Room

app = FastAPI(title="Elements Game Server", version="1.0.0")
manager = ConnectionManager()
rooms: dict[str, Room] = {}


@app.get("/")
async def read_root():
    '''Return server status and basic info'''
    return {"status": "online", "server": "Elements Game Server"}


@app.get("/rooms")
async def list_rooms():
    '''List all active game rooms'''
    return {"rooms": list(rooms.values())}


@app.post("/rooms", status_code=201)
async def create_room(name: str, max_players: int = 4):
    '''Create a new game room'''
    room_id = str(uuid.uuid4())
    room = Room(id=room_id, name=name, max_players=max_players)
    rooms[room_id] = room
    return room


@app.get("/rooms/{room_id}")
async def get_room(room_id: str):
    '''Get details for a specific room'''
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    return rooms[room_id]


@app.websocket("/ws/{room_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str):
    '''WebSocket endpoint for real-time multiplayer game communication'''
    if room_id not in rooms:
        await websocket.close(code=1008)
        return

    room = rooms[room_id]
    if len(room.players) >= room.max_players:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, room_id, player_id)
    room.players.add(player_id)

    await manager.broadcast(
        {"type": "player_joined", "player_id": player_id, "room_id": room_id},
        room_id,
    )

    try:
        while True:
            data = await websocket.receive_json()
            message = GameMessage(
                type=data.get("type", "unknown"),
                data=data.get("data"),
                player_id=player_id,
            )
            await manager.broadcast(message.model_dump(), room_id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id, player_id)
        room.players.discard(player_id)
        await manager.broadcast(
            {"type": "player_left", "player_id": player_id, "room_id": room_id},
            room_id,
        )
