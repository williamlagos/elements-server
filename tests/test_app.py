"""Tests for the Elements Game Server"""

import pytest
from fastapi.testclient import TestClient

from app import app, rooms

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_rooms():
    """Reset shared room state between tests"""
    rooms.clear()
    yield
    rooms.clear()


def test_read_root():
    """Server status endpoint returns online status"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "server" in data


def test_list_rooms_empty():
    """Room list is empty when no rooms have been created"""
    response = client.get("/rooms")
    assert response.status_code == 200
    assert response.json() == {"rooms": []}


def test_create_room():
    """Creating a room returns the new room object"""
    response = client.post("/rooms?name=TestRoom&max_players=2")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestRoom"
    assert data["max_players"] == 2
    assert "id" in data
    assert data["players"] == []


def test_list_rooms_after_creation():
    """Created rooms appear in the room list"""
    client.post("/rooms?name=Room1")
    response = client.get("/rooms")
    assert response.status_code == 200
    assert len(response.json()["rooms"]) == 1


def test_get_room():
    """Fetching a room by its ID returns correct details"""
    create_response = client.post("/rooms?name=MyRoom")
    room_id = create_response.json()["id"]

    response = client.get(f"/rooms/{room_id}")
    assert response.status_code == 200
    assert response.json()["id"] == room_id
    assert response.json()["name"] == "MyRoom"


def test_get_room_not_found():
    """Requesting a non-existent room returns 404"""
    response = client.get("/rooms/nonexistent-id")
    assert response.status_code == 404


def test_websocket_unknown_room():
    """Connecting to a WebSocket for a missing room closes the connection"""
    from starlette.websockets import WebSocketDisconnect

    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/bad-room/player1"):
            pass  # server should close immediately


def test_websocket_player_joined_and_left():
    """Player join and leave events are broadcast over WebSocket"""
    room_resp = client.post("/rooms?name=WSRoom")
    room_id = room_resp.json()["id"]

    with client.websocket_connect(f"/ws/{room_id}/player1") as ws:
        join_event = ws.receive_json()
        assert join_event["type"] == "player_joined"
        assert join_event["player_id"] == "player1"

    # After disconnect, room should no longer list the player
    assert "player1" not in rooms[room_id].players


def test_websocket_message_broadcast():
    """Messages sent by one player are broadcast back to the room"""
    room_resp = client.post("/rooms?name=BroadcastRoom")
    room_id = room_resp.json()["id"]

    with client.websocket_connect(f"/ws/{room_id}/player1") as ws:
        ws.receive_json()  # player_joined event

        ws.send_json({"type": "move", "data": {"x": 5, "y": 10}})
        msg = ws.receive_json()
        assert msg["type"] == "move"
        assert msg["data"] == {"x": 5, "y": 10}
        assert msg["player_id"] == "player1"


def test_websocket_room_full():
    """A player cannot join a full room"""
    from starlette.websockets import WebSocketDisconnect

    room_resp = client.post("/rooms?name=FullRoom&max_players=1")
    room_id = room_resp.json()["id"]

    with client.websocket_connect(f"/ws/{room_id}/player1") as ws:
        ws.receive_json()  # player_joined

        with pytest.raises(WebSocketDisconnect):
            with client.websocket_connect(f"/ws/{room_id}/player2"):
                pass  # server should reject the second player


def test_health_and_engine_status():
    """Health and engine status endpoints report engine metadata"""
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["engine"] == "elements"

    status = client.get("/api/engine/status")
    assert status.status_code == 200
    assert "cpp_accelerated" in status.json()


def test_waves_endpoint_returns_formation_and_waves():
    """Waves endpoint serves canonical or builtin Galaga formation and subwaves"""
    response = client.get("/api/waves")
    assert response.status_code == 200
    data = response.json()
    assert data["formation"]["cols"] == 10
    assert data["formation"]["rows"] == 4
    assert len(data["formation"]["layout"]) == 4
    assert len(data["waves"]) >= 1
    assert len(data["waves"][0]["subwaves"]) >= 1


def test_gb_sync_validates_dinamo_waves(tmp_path):
    """gb_sync projects waves onto 20x18 grid and checks actor budget"""
    import json
    from engine import gb_sync

    waves_file = tmp_path / "waves.json"
    waves_file.write_text(
        json.dumps(
            {
                "stage": 1,
                "formation": {
                    "cols": 10,
                    "rows": 4,
                    "slots": [
                        {"row": 0, "col": 3, "type": "boss"},
                        {"row": 0, "col": 4, "type": "boss"},
                        {"row": 1, "col": 1, "type": "butterfly"},
                        {"row": 2, "col": 1, "type": "bee"},
                    ],
                },
                "subwaves": [],
            }
        ),
        encoding="utf-8",
    )

    waves = gb_sync.load_waves(waves_file)
    report = gb_sync.validate_formation_on_grid(waves)
    assert report["grid_dims"] == (20, 18)
    assert report["gb_actor_count"] == 4
    assert report["within_actor_budget"] is True
    assert report["quadtree"].startswith("2")


def test_sensor_frame_normalization_endpoint():
    """POST /api/sensors normalizes IMU gyro/accel and SBC environmental readings"""
    resp = client.post(
        "/api/sensors",
        json={
            "device_id": "rpi-eos-runtime",
            "gyro": [0.2, 0.5, 0.0],
            "accel": [4.9, -2.0, 9.8],
            "proximity": 18.5,
            "ambient_light": 0.75,
            "temperature": 24.5,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["device_id"] == "rpi-eos-runtime"
    assert body["has_motion"] is True
    assert -1.0 <= body["tilt_x"] <= 1.0
    assert body["tilt_x"] > 0.0
    assert body["environment"]["proximity"] == 18.5
