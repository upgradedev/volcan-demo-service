# volcan-demo-service

A small FastAPI service with users, roles and workspaces.

This repository is demo material for the review walkthrough in the Volcan
accessibility demo. Volcan opens its pull requests and reads them aloud. It is
not production code and it is not maintained. Open pull requests here are
review material and are not meant to be merged.

## What it does

- `GET /workspaces` lists the workspaces the caller belongs to.
- `POST /workspaces` creates a workspace owned by the caller.
- `GET /workspaces/{id}` returns one workspace.
- `PATCH /workspaces/{id}` renames a workspace.
- `GET /health` reports that the service is up.

The caller is identified by the `X-User-Id` header, which an API gateway in
front of the service would set. Three users are seeded at start-up:
`u-admin` (admin), `u-member` (member) and `u-viewer` (viewer).

Data is kept in memory and is lost when the process stops.

## Run it

```bash
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Allowed CORS origins and methods come from `CORS_ORIGINS` and `CORS_METHODS`
(comma separated). The defaults are in `app/settings.py`.

## Test it

```bash
pytest
```

## Licence

MIT. See `LICENSE`.
