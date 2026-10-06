import pytest
from fastapi.testclient import TestClient

from app.main import create_app

MEMBER = {"X-User-Id": "u-member"}
VIEWER = {"X-User-Id": "u-viewer"}


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_unknown_user_is_rejected(client: TestClient) -> None:
    response = client.get("/workspaces", headers={"X-User-Id": "nobody"})
    assert response.status_code == 401


def test_member_creates_and_lists_a_workspace(client: TestClient) -> None:
    created = client.post("/workspaces", json={"name": "Design"}, headers=MEMBER)
    assert created.status_code == 201

    listed = client.get("/workspaces", headers=MEMBER)
    assert [w["name"] for w in listed.json()] == ["Design"]


def test_viewer_cannot_rename_a_workspace(client: TestClient) -> None:
    workspace = client.post("/workspaces", json={"name": "Design"}, headers=MEMBER).json()

    response = client.patch(
        f"/workspaces/{workspace['id']}", json={"name": "Renamed"}, headers=VIEWER
    )
    assert response.status_code == 403


def test_owner_deletes_a_workspace(client: TestClient) -> None:
    workspace = client.post("/workspaces", json={"name": "Scratch"}, headers=MEMBER).json()

    response = client.delete(f"/workspaces/{workspace['id']}", headers=MEMBER)
    assert response.status_code == 204
    assert client.get(f"/workspaces/{workspace['id']}", headers=MEMBER).status_code == 404


def test_deleting_an_unknown_workspace_returns_404(client: TestClient) -> None:
    response = client.delete("/workspaces/999", headers=MEMBER)
    assert response.status_code == 404
