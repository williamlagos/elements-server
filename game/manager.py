'''WebSocket connection manager for multiplayer sessions'''

from fastapi import WebSocket


class ConnectionManager:
    '''Manages active WebSocket connections grouped by game room'''

    def __init__(self):
        self.active_connections: dict[str, set[WebSocket]] = {}
        self.player_connections: dict[tuple[str, str], WebSocket] = {}

    async def connect(self, websocket: WebSocket, room_id: str, player_id: str):
        '''Accept a new WebSocket connection and register it to a room'''
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
        self.player_connections[(room_id, player_id)] = websocket

    async def disconnect(self, websocket: WebSocket, room_id: str, player_id: str):
        '''Remove a WebSocket connection from the room registry'''
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
        self.player_connections.pop((room_id, player_id), None)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        '''Send a JSON message to a single connection'''
        await websocket.send_json(message)

    async def broadcast(self, message: dict, room_id: str):
        '''Broadcast a JSON message to all connections in a room'''
        for connection in self.active_connections.get(room_id, set()):
            await connection.send_json(message)
