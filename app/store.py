"""In-memory records for users and workspaces.

A real deployment would keep these in a database. The demo keeps them in
memory so it runs with nothing else installed.
"""
from dataclasses import dataclass, field
from enum import Enum
from itertools import count

from fastapi import Request


class Role(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


@dataclass(frozen=True)
class User:
    id: str
    name: str
    role: Role


@dataclass
class Workspace:
    id: int
    name: str
    owner_id: str
    member_ids: set[str] = field(default_factory=set)


class Store:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._workspaces: dict[int, Workspace] = {}
        self._next_id = count(1)

    def add_user(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def create_workspace(self, name: str, owner: User) -> Workspace:
        workspace = Workspace(
            id=next(self._next_id), name=name, owner_id=owner.id, member_ids={owner.id}
        )
        self._workspaces[workspace.id] = workspace
        return workspace

    def get_workspace(self, workspace_id: int) -> Workspace | None:
        return self._workspaces.get(workspace_id)

    def workspaces_for(self, user: User) -> list[Workspace]:
        return [w for w in self._workspaces.values() if user.id in w.member_ids]

    def delete_workspace(self, workspace_id: int) -> None:
        self._workspaces.pop(workspace_id, None)


def seeded_store() -> Store:
    store = Store()
    store.add_user(User("u-admin", "Alex", Role.ADMIN))
    store.add_user(User("u-member", "Sam", Role.MEMBER))
    store.add_user(User("u-viewer", "Riya", Role.VIEWER))
    return store


def get_store(request: Request) -> Store:
    """FastAPI dependency: the store created with the app."""
    return request.app.state.store
