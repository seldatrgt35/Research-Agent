# Research Agent Platform

Production-grade foundation for a future multi-agent AI research platform. This repository currently contains only the project foundation: configuration, FastAPI wiring, dependency injection seams, logging, database scaffolding, Alembic scaffolding, Docker assets, and one health endpoint.

The codebase is intentionally not implementing RAG, embeddings, LLM calls, agents, repository cloning, tree-sitter, tool calling, vector search, or research workflows yet.

## Current Capability

- `GET /health`
- Response:

```json
{
  "status": "healthy"
}
```

## Architectural Direction

The architecture is inspired at a high level by:

- [OpenHands](https://github.com/OpenHands/OpenHands), for clear platform boundaries and self-hostable operational concerns.
- [CodeScout](https://github.com/OpenHands/codescout), for the future need to support repository and code-intelligence workflows without coupling those workflows to HTTP.
- [DeepWiki Open](https://github.com/AsyncFuncAI/deepwiki-open), for the future documentation/report-generation direction.

No code has been copied from those projects.

## Folder Structure

```text
.
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── src/
│   └── research_agent/
│       ├── application/
│       │   └── health/
│       ├── core/
│       ├── domain/
│       ├── infrastructure/
│       │   └── database/
│       ├── interfaces/
│       │   └── api/
│       └── main.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Package Responsibilities

`src/research_agent/main.py` is the application composition root. It creates the FastAPI app, configures logging, wires routers, registers exception handlers, and initializes infrastructure resources during lifespan startup.

`src/research_agent/core/` contains cross-cutting primitives that are not business workflows: settings, logging configuration, and the base application exception. This keeps operational concerns reusable without making them depend on FastAPI.

`src/research_agent/domain/` is reserved for enterprise business concepts and rules. Future repository, paper, project, document, report, and research-session entities should live here when they represent stable domain behavior.

`src/research_agent/application/` contains use-case orchestration. Today it has only the health-check use case. Future services that coordinate repository analysis, paper analysis, report generation, or multi-agent workflows should live here behind explicit interfaces.

`src/research_agent/infrastructure/` contains outbound adapters for external systems. Database setup lives here now. Future provider SDKs, GitHub clients, browser/search providers, file storage, queues, LLM clients, embedding providers, and vector-store adapters should be added here behind interfaces owned by the application layer.

`src/research_agent/interfaces/` contains inbound adapters. The current adapter is FastAPI HTTP. Future CLI commands, worker entrypoints, webhook handlers, or scheduler entrypoints can be added here without changing domain code.

`src/research_agent/interfaces/api/` owns HTTP routing, dependency providers, and exception translation. It should remain thin: validation, request/response mapping, and delegation to application services only.

`alembic/` contains database migration scaffolding. It is wired to the shared SQLAlchemy metadata and settings, but no migrations are present because there are no domain models yet.

`tests/` contains automated tests. The current test verifies the public health endpoint through FastAPI's test client.

## Architectural Decisions

The project uses a `src/` layout so imports behave the same in tests, local development, Docker builds, and installed environments.

FastAPI is treated as an inbound adapter, not the center of the system. API route modules call application services and do not contain business logic.

Settings use `pydantic-settings` with a `RESEARCH_AGENT_` prefix and nested environment keys such as `RESEARCH_AGENT_DATABASE__URL`. This keeps runtime configuration explicit and avoids hardcoded provider choices.

The app is built through `create_app(settings: Settings | None = None)`. Tests and future deployments can inject settings without mutating module-level configuration.

Database setup uses SQLAlchemy 2 async engine and session factories. The engine is created during FastAPI lifespan startup and disposed cleanly on shutdown.

Alembic is configured now, but migrations are intentionally empty. Schema evolution can begin when real domain models exist.

PostgreSQL runs through the `pgvector/pgvector:pg16` image in Docker Compose. This prepares the platform for later vector capabilities without implementing vector search in this iteration.

Logging is configured centrally with plain and JSON formats. JSON logging can be enabled in production without changing application code.

Exceptions have a small hierarchy rooted in `AppError`. API exception handlers translate application errors into consistent JSON responses while keeping HTTP details out of domain and application code.

Dependency injection is centralized in `interfaces/api/dependencies.py`. This gives future services and repositories a single place to be wired into HTTP routes.

## Local Development

Create an environment file:

```bash
cp .env.example .env
```

Install dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the API:

```bash
uvicorn research_agent.main:app --reload
```

Run tests:

```bash
pytest
```

Run with Docker Compose:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

