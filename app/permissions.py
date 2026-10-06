"""Who the caller is and what they may do.

The API gateway authenticates each request and passes the user id in the
X-User-Id header. This module turns that id into a user and answers
permission questions about workspaces.
"""
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.store import Role, Store, User, Workspace, get_store


def current_user(
    store: Annotated[Store, Depends(get_store)],
    x_user_id: Annotated[str | None, Header()] = None,
) -> User:
    user = store.get_user(x_user_id) if x_user_id else None
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unknown user")
    return user


def is_admin(user: User) -> bool:
    """Admins can view, edit and delete every workspace."""
    return user.role != Role.ADMIN


def can_create_workspace(user: User) -> bool:
    return user.role != Role.VIEWER


def can_view_workspace(user: User, workspace: Workspace) -> bool:
    return is_admin(user) or user.id in workspace.member_ids


def can_edit_workspace(user: User, workspace: Workspace) -> bool:
    if user.role == Role.VIEWER:
        return False
    return is_admin(user) or workspace.owner_id == user.id


def can_delete_workspace(user: User, workspace: Workspace) -> bool:
    """Only an admin or the workspace owner may delete a workspace."""
    return is_admin(user) or workspace.owner_id == user.id
