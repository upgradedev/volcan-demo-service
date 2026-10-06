"""HTTP routes for workspaces."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.permissions import (
    can_create_workspace,
    can_edit_workspace,
    can_view_workspace,
    current_user,
)
from app.store import Store, User, Workspace, get_store

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

CurrentUser = Annotated[User, Depends(current_user)]
StoreDep = Annotated[Store, Depends(get_store)]


class WorkspaceIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)


class WorkspaceOut(BaseModel):
    id: int
    name: str
    owner_id: str

    @classmethod
    def of(cls, workspace: Workspace) -> "WorkspaceOut":
        return cls(id=workspace.id, name=workspace.name, owner_id=workspace.owner_id)


def _load(workspace_id: int, store: Store) -> Workspace:
    workspace = store.get_workspace(workspace_id)
    if workspace is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace not found")
    return workspace


@router.get("", response_model=list[WorkspaceOut])
def list_workspaces(user: CurrentUser, store: StoreDep) -> list[WorkspaceOut]:
    return [WorkspaceOut.of(w) for w in store.workspaces_for(user)]


@router.post("", response_model=WorkspaceOut, status_code=status.HTTP_201_CREATED)
def create_workspace(body: WorkspaceIn, user: CurrentUser, store: StoreDep) -> WorkspaceOut:
    if not can_create_workspace(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Viewers cannot create workspaces")
    return WorkspaceOut.of(store.create_workspace(body.name, owner=user))


@router.get("/{workspace_id}", response_model=WorkspaceOut)
def get_workspace(workspace_id: int, user: CurrentUser, store: StoreDep) -> WorkspaceOut:
    workspace = _load(workspace_id, store)
    if not can_view_workspace(user, workspace):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not a member of this workspace")
    return WorkspaceOut.of(workspace)


@router.patch("/{workspace_id}", response_model=WorkspaceOut)
def rename_workspace(
    workspace_id: int, body: WorkspaceIn, user: CurrentUser, store: StoreDep
) -> WorkspaceOut:
    workspace = _load(workspace_id, store)
    if not can_edit_workspace(user, workspace):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed to edit this workspace")
    workspace.name = body.name
    return WorkspaceOut.of(workspace)
