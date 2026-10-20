"""Security regression tests for authentication and authorization."""
from tests.conftest import login, auth


def test_protected_route_rejects_no_token(client):
    res = client.get("/notes")
    assert res.status_code == 401


def test_protected_route_rejects_bad_token(client):
    res = client.get("/notes", headers=auth("not.a.jwt"))
    assert res.status_code == 401


def test_user_cannot_read_another_users_note(client):
    alice_token = login(client, "alice", "alicepass")
    assert alice_token is not None
    res = client.get("/notes/2", headers=auth(alice_token))
    assert res.status_code == 403


def test_user_can_read_own_note(client):
    alice_token = login(client, "alice", "alicepass")
    assert alice_token is not None
    res = client.get("/notes/1", headers=auth(alice_token))
    assert res.status_code == 200
    assert res.json()["title"] == "Alice diary"


def test_login_does_not_reveal_which_field_was_wrong(client):
    unknown_user = client.post(
        "/login", json={"username": "unknown", "password": "bad-password"}
    )
    incorrect_password = client.post(
        "/login", json={"username": "alice", "password": "bad-password"}
    )
    assert unknown_user.status_code == 401
    assert incorrect_password.status_code == 401
    assert unknown_user.json() == incorrect_password.json()


def test_non_admin_cannot_list_users(client):
    alice_token = login(client, "alice", "alicepass")
    assert alice_token is not None
    res = client.get("/admin/users", headers=auth(alice_token))
    assert res.status_code == 403


def test_admin_can_list_users_without_password_leak(client):
    admin_token = login(client, "admin", "admin123")
    assert admin_token is not None
    res = client.get("/admin/users", headers=auth(admin_token))
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 3
    assert all(set(user.keys()) == {"id", "username", "is_admin"} for user in users)
    assert any(user["username"] == "admin" and user["is_admin"] for user in users)
