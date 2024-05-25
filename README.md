# Python Starter

Python Starter app setup suing

- Python (python)
- sqlAlchemy (ORM)
- psycopg2-binary (PostgreSQL database adapter)
- alembic (db migration tool)
- fastapi (api)
- pydantic (data validation and settings management library. It is one of FastAPI dependencies)
- uvicorn (ASGI web server implementation)
- dependency-injector (DI framework)
- structlog and colorlog (logger)
- black (formatter)
- flake8 (linter and checker)
- ruff (linter)
- mypy (static type checker)

# Pre-requisite

All dependencies are pre-install via nix and activated via direnv

- Nix > 2.12.0
- direnv > 2.23.2
- Docker

# Directory

```
.
├── config
│   └── ...                 # tooling configuration
├── nix
│   └── ...                 # environment configuration
├── scripts
│   └── ...                 # scripts for automation and CI
├── infra
│   └── ...                 # Docker, Helm and related infrastucture
├── alembic
│   └── ...                 # Database migrations for each database
├── src
│   ├── routers
│   │   └── v1             # API endpoints, requests and response payload
│   |        ├── endpoints.py
│   │        ├── requests.py
│   │        └── response.py
│   ├── modules
│   │   └── ...             # business domains
│   ├── registry
│   │   └── ...             # IoC registration
│   ├── system
│   │   └── ...             # server and logger setup
│   └── api.ts              # create setup
│
└── tests
    ├── integartion
    │   └── ...             # integration tests here
    └── unit
        └── ...             # unit tests here
```

# Running locally

Run codes locally

- `poetry run python src/.../main.py`

Start Jupyter Notebook

- `poetry run jupyter notebook`

# Quality Assurance

Run ruff linter

- `ruff check .`

# Git Commit

Read `atomi_release.yaml` under `types` on how to do git commit for semantic release
