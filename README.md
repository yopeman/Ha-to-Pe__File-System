# Ha-to-Pe File System

A multi-user, permission-aware virtual file system. Users manage files and directories through a **web app**, **mobile app**, **desktop app**, and/or a **terminal shell** — all backed by one API with sharing, real-time collaboration, trash, compression, and storage quotas.

> **Status:** Planning and documentation complete; implementation starting with backend Phase 0.

---

## Features

- **Accounts** — OAuth 2.0 (Google, GitHub) and email/password
- **File system** — Files, directories, and zip archives in a logical tree
- **Upload / download** — Streaming REST API with quota enforcement
- **Trash** — Soft delete, restore, permanent delete, empty trash
- **Search** — By name (current directory or global)
- **Sharing** — Private, shared (invitation), and public directories with ACL inheritance
- **Real-time** — Live directory updates and presence in shared folders
- **CLI** — Virtual shell (`cd`, `ls`, `upload`, `download`, …) over the API
- **Admin** — Default quota, analytics, storage upgrades

---

## Repository Structure

```
Ha-to-Pe__File-System/
├── backend/              # FastAPI + Ariadne + SQLAlchemy (Python 3.12+)
├── frontend-web/         # React + Vite (planned)
├── frontend-mobile/      # React Native + Expo (planned)
├── frontend-desktop/     # Electron (planned)
├── cli/                  # Python CLI / virtual shell (planned)
├── packages/shared/      # Shared API types and hooks (planned)
└── docs/                 # Requirements, schema, API, implementation plans
```

---

## Tech Stack

| Layer | Technologies |
|-------|----------------|
| Backend | Python, FastAPI, Ariadne, SQLAlchemy, MySQL/SQLite, UV, pytest |
| API | GraphQL (metadata) + REST (upload/download, auth) |
| Web | React, Vite, TypeScript, Apollo Client, Tailwind |
| Mobile | React Native, Expo, EAS |
| Desktop | Electron, electron-vite, React |
| CLI | Python, Typer, Rich, httpx |

Details: [docs/tech_stack.md](docs/tech_stack.md)

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/requirement.md](docs/requirement.md) | Functional and non-functional requirements |
| [docs/usecase.md](docs/usecase.md) | Use cases (UC-01–UC-33) with flows |
| [docs/db_schema.md](docs/db_schema.md) | Database tables, ERD, DDL, queries |
| [docs/api.md](docs/api.md) | **API contract** — GraphQL schema, REST, auth, errors |
| [docs/tech_stack.md](docs/tech_stack.md) | Technologies and architecture conventions |

### Implementation Plans

| Document | Client / layer |
|----------|----------------|
| [docs/backend_implementation_plan.md](docs/backend_implementation_plan.md) | Backend (Phases 0–5) |
| [docs/web_app_implementation_plan.md](docs/web_app_implementation_plan.md) | Web app (W0–W5) |
| [docs/mobile_app_implementation_plan.md](docs/mobile_app_implementation_plan.md) | Mobile app (M0–M5) |
| [docs/desktop_app_implementation_plan.md](docs/desktop_app_implementation_plan.md) | Desktop app (D0–D5) |
| [docs/cli_implementation_plan.md](docs/cli_implementation_plan.md) | CLI (C0–C5) |

**Suggested read order:** requirements → API → backend plan → client plan for your surface.

---

## Getting Started (Local Development)

Prerequisites: **Python 3.12+**, **[UV](https://docs.astral.sh/uv/)**, **Node.js 20+** (for frontends, when added).

### Backend

```bash
cd backend
uv sync --extra dev
cp .env.example .env          # when available
uv run alembic upgrade head   # when migrations exist
uv run uvicorn app.main:app --reload --port 8000
```

- GraphQL: `http://localhost:8000/graphql`
- REST / OpenAPI: `http://localhost:8000/docs`

### Web (when scaffolded)

```bash
cd frontend-web
npm install
npm run codegen               # GraphQL types from backend schema
npm run dev                   # http://localhost:5173
```

### CLI (when scaffolded)

```bash
cd cli
uv sync --extra dev
uv run hatope login
uv run hatope shell
```

Environment variables are documented in [docs/api.md](docs/api.md) and per-client implementation plans.

---

## Implementation Phases

Development proceeds in layers. Each phase should be end-to-end testable before the next.

| Phase | Backend | Clients |
|-------|---------|---------|
| **0** | Scaffold, auth, user + root directory | Web/desktop/mobile login shell |
| **1** | Private FS, upload/download, trash, search | File manager UI, CLI core commands |
| **2** | Sharing, permissions, public links | Share dialogs, invitations |
| **3** | GraphQL subscriptions, presence | Live updates in shared dirs |
| **4** | Zip/unzip, path resolution | Archive flows, CLI full paths |
| **5** | Admin, analytics, billing | Admin dashboard, storage upgrade |

Start with **backend Phase 0**, then **web W0–W1**. Mobile, desktop, and CLI follow once the API is stable.

---

## API Overview

- **GraphQL** — Tree navigation, mutations, search, sharing, subscriptions
- **REST** — `POST /auth/*`, upload sessions, `GET /download/{id}`
- **Auth** — JWT access token + refresh token

Full reference: [docs/api.md](docs/api.md)

---

## Contributing

1. Read [docs/requirement.md](docs/requirement.md) and [docs/backend_implementation_plan.md](docs/backend_implementation_plan.md) for the current phase.
2. Follow the layered backend rule: `domain` → `services` → `api`.
3. Format Python with `black` and `isort`; use `ruff` for linting.
4. Add tests for service-layer logic before merging features.

---

## License

TBD
