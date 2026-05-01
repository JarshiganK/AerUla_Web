# AerUla Stack Setup Todo

## Completed

- [x] Initialized Git repository in `D:\Projects\YIT`.
- [x] Created `.venv` virtual environment folder.
- [x] Installed Django into `.venv\Lib\site-packages`.
- [x] Installed `psycopg[binary]` into `.venv\Lib\site-packages`.
- [x] Installed `python-dotenv` into `.venv\Lib\site-packages`.
- [x] Created Django project `aerula`.
- [x] Created apps: `core`, `accounts`, `village`, `simulations`, `bookings`, `marketplace`, `dashboard`.
- [x] Added `.env.example`, `.env`, `.gitignore`, `requirements.txt`, and `README.md`.
- [x] Configured Django for local PostgreSQL through environment variables.
- [x] Added Bootstrap CDN to `templates/base.html`.
- [x] Added starter home page at `/`.
- [x] Added placeholder app routes for accounts, village, simulations, bookings, marketplace, and dashboard.
- [x] Added static files: `static/css/site.css` and `static/js/village.js`.
- [x] Confirmed `python --version`: Python 3.13.3.
- [x] Confirmed `git --version`: Git 2.43.0.
- [x] Confirmed Django in project venv: Django 6.0.4.
- [x] Confirmed `npm.cmd --version`: npm 10.9.3.
- [x] Confirmed PostgreSQL client: PostgreSQL 17.6 at `C:\Program Files\PostgreSQL\17\bin\psql.exe`.
- [x] Confirmed `python manage.py check` passes.
- [x] Added `scripts\setup_postgres.ps1` to create/update the PostgreSQL user and database from `.env`.
- [x] Added `scripts\init_dev.ps1` to run database setup, Django checks, migrations, and optional dev server startup.

## Blocked Until PostgreSQL Admin Password Is Entered

- [ ] Run `.\scripts\init_dev.ps1`.
- [ ] Enter the local PostgreSQL `postgres` admin password when prompted.
- [ ] Confirm the script creates or updates values from `.env`:
  - database: `aerula_db`
- [ ] Confirm migrations complete.
- [ ] Run `.\scripts\init_dev.ps1 -RunServer` or `.venv\Scripts\python manage.py runserver`.
- [ ] Open `http://127.0.0.1:8000/`.

## Notes

- `npm` is blocked directly in PowerShell by execution policy, but `npm.cmd` works.
- `psql` is installed but not on PATH, so the setup script uses the full PostgreSQL path.
- The local Python install has an `ensurepip` permission issue. Dependencies were installed into `.venv\Lib\site-packages` using global `pip --target`, so project Python commands still work.
- `.tmp` contains locked temporary folders created by the failed `ensurepip` run and is ignored by Git.
