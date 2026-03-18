# Elements Game Server

A modern asyncio-powered multiplayer game server built with [FastAPI](https://fastapi.tiangolo.com/) and WebSockets.

## Features

- **REST API** for room management (create, list, inspect rooms)
- **WebSocket** endpoint for real-time multiplayer communication
- **Async** throughout – built on Python's `asyncio` via ASGI/Uvicorn
- **Pydantic v2** models for type-safe data exchange

## Requirements

- Python 3.12+
- Dependencies listed in `requirements.txt`

## Setup

```bash
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn app:app --reload
```

The server starts at `http://127.0.0.1:8000`.  
Interactive docs are available at `http://127.0.0.1:8000/docs`.

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Server status |
| `GET` | `/rooms` | List active rooms |
| `POST` | `/rooms?name=<name>&max_players=<n>` | Create a room |
| `GET` | `/rooms/{room_id}` | Room details |
| `WS` | `/ws/{room_id}/{player_id}` | Real-time game channel |

## WebSocket Protocol

Connect to `/ws/{room_id}/{player_id}` after creating or choosing a room.

**Server events sent to clients:**

```json
{ "type": "player_joined", "player_id": "...", "room_id": "..." }
{ "type": "player_left",   "player_id": "...", "room_id": "..." }
```

**Client messages (forwarded to all room members):**

```json
{ "type": "move", "data": { "x": 10, "y": 20 } }
```

## Development

Install dev dependencies and run tests:

```bash
pip install -r requirements-dev.txt
pytest
```

## License

GNU Lesser General Public License v3 – see [LICENSE](LICENSE) for details.
