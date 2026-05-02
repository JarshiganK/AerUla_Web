# AerUla MVP

AerUla is a Django-based web platform for a browser-based cultural village simulation, role-based dashboards, bookings, and a marketplace.

## Local Stack

- Python 3.13
- Django 6
- PostgreSQL 17
- Bootstrap 5 via CDN
- JavaScript/SVG/Canvas for simulation interactions

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

This machine currently has a Python `ensurepip` permission issue. If venv pip creation fails, install dependencies into the venv target:

```powershell
pip install --target .venv\Lib\site-packages -r requirements.txt
```

PostgreSQL is installed locally, but `psql.exe` may need to be called by full path:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres
```

Create the database from `.env`, run checks, apply migrations, and optionally start the server:

```powershell
.\scripts\init_dev.ps1
.\scripts\init_dev.ps1 -RunServer
```

If PowerShell blocks the setup script, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Or use a one-time process bypass without changing your user policy:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init_dev.ps1
```

By default, the script uses `POSTGRES_USER` and `POSTGRES_PASSWORD` from `.env` to create `POSTGRES_DB`. If that user cannot create databases, run it with a PostgreSQL admin account:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init_dev.ps1 -PostgresAdminUser postgres
```

If the database and user already exist and only migrations are needed:

```powershell
.\scripts\init_dev.ps1 -SkipDbInit
```

## Playwright E2E Tests

Install the browser test dependencies once:

```powershell
cmd /c npm install
cmd /c npx playwright install chromium
```

Run the browser regression suite. Playwright starts a fresh Django dev server on port 8123 automatically and runs desktop and mobile Chromium projects:

```powershell
cmd /c npm run test:e2e
```
