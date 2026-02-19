# HomeLab Media Hub

Project for collecting and storing media content from creators (RSS/feeds).

Quick start

- Create a `.env` file in the `backend/` folder (see `env.example`).
- Start services (Docker Desktop required):

```powershell
docker compose up -d --build
docker compose logs -f backend
```

- The API will be available at: http://localhost:8000
- Health endpoint: http://localhost:8000/health

Running tests (local, inside a virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements_dev.txt
pytest -q
```

Repository layout

- `backend/` — FastAPI application, models, health endpoint
- `docker-compose.yaml` — defines Postgres, RSS-Bridge, backend services
- `requirements.txt` / `requirements_dev.txt` — runtime and dev dependencies

License

- MIT
