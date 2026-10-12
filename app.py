"""
Elements Game Server
Asyncio-powered multiplayer server and Unified Arcade API for Dinamo & Elements Engine
"""

import json
import os
import time
import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from game.manager import ConnectionManager
from game.models import GameMessage, Room

app = FastAPI(
    title="Elements Game Server",
    description="Multiplayer Rooms, Game API, and Universal Leaderboard for Elements & Dinamo",
    version="1.0.0"
)

# Enable CORS for browser Web clients (e.g. Vite on localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()
rooms: dict[str, Room] = {}

LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard.json")

# Default arcade high scores
DEFAULT_SCORES = [
    {"player": "ACE", "score": 50000, "stage": 5, "platform": "arcade", "timestamp": int(time.time()) - 86400 * 3},
    {"player": "NAM", "score": 35000, "stage": 4, "platform": "apple", "timestamp": int(time.time()) - 86400 * 2},
    {"player": "PIX", "score": 25000, "stage": 3, "platform": "web", "timestamp": int(time.time()) - 86400},
    {"player": "ELM", "score": 20000, "stage": 2, "platform": "elements", "timestamp": int(time.time()) - 3600},
    {"player": "GAL", "score": 15000, "stage": 1, "platform": "arcade", "timestamp": int(time.time()) - 1800},
]


def load_scores() -> list:
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_SCORES.copy()
    return DEFAULT_SCORES.copy()


def save_scores(scores: list):
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")


# Pydantic Schemas
class ScoreEntry(BaseModel):
    player: str = Field(..., max_length=5, min_length=1, description="Player initials (e.g. AAA)")
    score: int = Field(..., ge=0, description="Final score achieved")
    stage: int = Field(default=1, ge=1, description="Stage reached")
    platform: str = Field(default="web", description="Client platform: apple, web, android, gb")


class LeaderboardResponse(BaseModel):
    total: int
    scores: list


# --- Basic & Health Endpoints ---

@app.get("/")
async def read_root():
    """Return server status and basic info"""
    return {
        "status": "online",
        "server": "Elements Game Server",
        "endpoints": ["/rooms", "/api/health", "/api/waves", "/api/leaderboard"]
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "online",
        "engine": "elements",
        "version": "1.0.0",
        "timestamp": int(time.time())
    }


# --- Arcade Waves & Leaderboard Endpoints ---

@app.get("/api/waves")
async def get_wave_config():
    """Returns standardized Galaga formation and entrance wave specifications"""
    return {
        "formation": {
            "cols": 10,
            "rows": 4,
            "colSpacing": 36,
            "rowSpacing": 28,
            "layout": [
                {"row": 0, "cols": [3, 4, 5, 6], "type": "boss", "health": 2, "points": 150, "divePoints": 400},
                {"row": 1, "cols": [1, 2, 3, 4, 5, 6, 7, 8], "type": "butterfly", "health": 1, "points": 80, "divePoints": 160},
                {"row": 2, "cols": [1, 2, 3, 4, 5, 6, 7, 8], "type": "bee", "health": 1, "points": 50, "divePoints": 100},
                {"row": 3, "cols": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "type": "bee", "health": 1, "points": 50, "divePoints": 100}
            ]
        },
        "waves": [
            {
                "waveIndex": 1,
                "subwaves": [
                    {"type": "boss", "row": 0, "col": 4, "path": "topLeft", "delay": 0.15},
                    {"type": "boss", "row": 0, "col": 5, "path": "topRight", "delay": 0.35},
                    {"type": "boss", "row": 0, "col": 3, "path": "topLeft", "delay": 0.55},
                    {"type": "boss", "row": 0, "col": 6, "path": "topRight", "delay": 0.75},
                    {"type": "butterfly", "row": 1, "col": 4, "path": "topLeft", "delay": 0.95},
                    {"type": "butterfly", "row": 1, "col": 5, "path": "topRight", "delay": 1.15},
                    {"type": "butterfly", "row": 1, "col": 3, "path": "topLeft", "delay": 1.35},
                    {"type": "butterfly", "row": 1, "col": 6, "path": "topRight", "delay": 1.55}
                ]
            }
        ]
    }


@app.get("/api/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(limit: int = 10):
    """Returns top global arcade high scores sorted descending"""
    scores = load_scores()
    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:limit]

    for idx, item in enumerate(sorted_scores, 1):
        item["rank"] = idx

    return {
        "total": len(sorted_scores),
        "scores": sorted_scores
    }


@app.post("/api/leaderboard")
async def submit_score(entry: ScoreEntry):
    """Submits a new arcade score to the global leaderboard"""
    scores = load_scores()
    new_entry = {
        "player": entry.player.upper().strip(),
        "score": entry.score,
        "stage": entry.stage,
        "platform": entry.platform.lower().strip(),
        "timestamp": int(time.time())
    }
    scores.append(new_entry)
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:50]
    save_scores(scores)

    rank = next((idx + 1 for idx, s in enumerate(scores) if s == new_entry), len(scores))

    return {
        "message": "Score recorded successfully",
        "rank": rank,
        "entry": new_entry
    }


# --- Multiplayer Room Endpoints ---

@app.get("/rooms")
async def list_rooms():
    """List all active game rooms"""
    return {"rooms": list(rooms.values())}


@app.post("/rooms", status_code=201)
async def create_room(name: str, max_players: int = 4):
    """Create a new game room"""
    room_id = str(uuid.uuid4())
    room = Room(id=room_id, name=name, max_players=max_players)
    rooms[room_id] = room
    return room


@app.get("/rooms/{room_id}")
async def get_room(room_id: str):
    """Get details for a specific room"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    return rooms[room_id]


@app.websocket("/ws/{room_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str):
    """WebSocket endpoint for real-time multiplayer game communication"""
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
