"""API behavior tests for SecureNotes."""
from tests.conftest import login, auth


def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


def test_register_then_login(client):
    res = client.post("/register", json={"username": "charlie", "password": "charliepass"})
    assert res.status_code == 200

    res = client.post("/login", json={"username": "charlie", "password": "charliepass"})
    assert res.status_code == 200
    data = res.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert data["access_token"].count(".") == 2


def test_login_wrong_password_is_401(client):
    res = client.post("/login", json={"username": "alice", "password": "wrong-password"})
    assert res.status_code == 401


def test_create_then_list_own_note(client):
    token = login(client, "alice", "alicepass")
    assert token is not None
    res = client.post(
        "/notes",
        json={"title": "My new note", "body": "Visible only to Alice"},
        headers=auth(token),
    )
    assert res.status_code == 200
    note_id = res.json()["id"]

    res = client.get("/notes", headers=auth(token))
    assert res.status_code == 200
    assert any(note["id"] == note_id and note["title"] == "My new note" for note in res.json())
