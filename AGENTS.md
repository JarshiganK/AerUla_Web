# AGENTS.md

Guidance for coding agents working on AerUla Web.

## Project Context

AerUla is a web platform for a browser-based Sri Lankan cultural village simulation. The MVP currently uses:

- Django backend with PostgreSQL.
- Django templates with Bootstrap for responsive UI.
- JavaScript, SVG, and Canvas for lightweight simulation interactions.
- Apps split by product area: `accounts`, `village`, `simulations`, `bookings`, `marketplace`, `dashboard`, and `core`.

The planned deployment split is:

- Backend/API/admin: AWS.
- Frontend web experience: Vercel.
- Database: managed PostgreSQL, preferably Amazon RDS.
- Media/static production assets: S3/CloudFront or a deliberate Vercel/AWS split documented before implementation.

Read `prd.md` before making product or architecture decisions. Keep the MVP focused on 2D browser simulation, learning, badges/passport, marketplace, bookings, and admin workflows.

When changing architecture, deployment flow, app boundaries, testing policy, security posture, or frontend/backend responsibilities, update this `AGENTS.md` file in the same change. Do not let implementation drift away from these instructions.

## Local Development Commands

Use PowerShell from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init_dev.ps1 -SkipDbInit
.\.venv\Scripts\python.exe manage.py runserver
```

When database credentials change:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init_dev.ps1
```

Before finishing changes, run:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

Testing is mandatory for all behavior changes. Do not treat tests as optional cleanup.

If migrations are added, also run:

```powershell
.\.venv\Scripts\python.exe manage.py makemigrations --check
.\.venv\Scripts\python.exe manage.py migrate
```

## Security Rules

- Never commit `.env`, real secrets, database passwords, AWS keys, private keys, or downloaded production data.
- Keep secrets in environment variables or AWS Secrets Manager / SSM Parameter Store.
- `DEBUG` must be `False` in AWS production.
- `DJANGO_SECRET_KEY` must be unique per environment and never use the local fallback in production.
- `ALLOWED_HOSTS` must explicitly include only the production domain, load balancer DNS name if needed, and approved staging domains.
- Configure CSRF trusted origins for deployed HTTPS domains.
- Use HTTPS only in production. Enable secure cookies, HSTS, proxy SSL header, and CSRF/session cookie security before launch.
- Do not expose Django admin publicly without strong protections. At minimum use strong staff passwords; preferably restrict by network, VPN, or additional authentication.
- Validate all user input server-side, especially bookings, orders, product forms, host applications, uploads, and simulation score submissions.
- Do not trust client-side simulation scores. Recalculate or validate completion state on the server before awarding badges.
- Use Django permissions, groups, or explicit role checks for tourist, host, admin, and super admin flows.
- File uploads must validate content type, size, extension, and storage destination.
- Avoid raw SQL. If raw SQL is required, use parameterized queries only.
- Keep dependencies pinned in `requirements.txt` and review upgrades before production deployment.

## Deployment Expectations

Frontend deployment is planned for Vercel. Backend deployment is planned for AWS. Do not assume a single-server Django template deployment for production without confirming the architecture.

### Vercel Frontend

When a separate frontend is introduced, prefer a professional React/Next.js frontend deployed on Vercel. Keep the frontend cleanly separated from Django backend concerns.

- Store public frontend environment variables with the `NEXT_PUBLIC_` prefix only when they are safe to expose.
- Keep API base URLs environment-specific, such as local, preview, staging, and production.
- Do not store backend secrets, AWS keys, database credentials, private API keys, or service tokens in Vercel client-exposed variables.
- Use Vercel preview deployments for review before production promotion.
- Configure production domain, HTTPS, redirects, and security headers intentionally.
- Use image optimization and responsive images for cultural hut artwork, marketplace products, and public pages.
- Keep frontend builds deterministic: lock package versions and commit lockfiles when a Node frontend is added.
- Frontend must handle backend API errors gracefully with clear user messages, loading states, and empty states.
- Authentication architecture must be explicit before implementation: cookie/session auth with correct CORS/CSRF settings, or token-based auth with secure storage rules.

### AWS Backend

Preferred production shape:

- Compute: Elastic Beanstalk, ECS Fargate, or EC2 with a managed process supervisor. For this MVP, choose the simplest maintainable option first.
- Database: Amazon RDS for PostgreSQL, not a database running inside the app server.
- Static files: S3 plus CloudFront, or WhiteNoise only for a very small early demo. Prefer S3/CloudFront for production.
- Media uploads: S3 private bucket with controlled access; do not store user media on ephemeral app disks.
- Secrets: AWS Secrets Manager or SSM Parameter Store.
- Logs: CloudWatch Logs.
- Email: Amazon SES or another verified provider.
- Domain/TLS: Route 53 plus ACM certificate behind an HTTPS load balancer or CloudFront for AWS-hosted backend endpoints.
- Backups: enable automated RDS backups and define retention before launch.

Production Django settings should be separated from local settings or driven safely by environment variables. Do not hardcode AWS resource names, credentials, hostnames, or secrets in code.

Required production environment variables should include:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `CSRF_TRUSTED_ORIGINS`
- `AWS_STORAGE_BUCKET_NAME` when S3 media/static storage is implemented

Before any AWS launch, add and verify:

- `collectstatic` workflow.
- Production static/media storage.
- Production logging.
- Health check URL.
- Migration command in deployment process.
- Superuser creation process that does not expose credentials.
- Backup and restore notes for RDS.
- CORS and CSRF settings compatible with the Vercel frontend domain.
- API versioning or clear endpoint naming if Django serves JSON APIs for the frontend.

## Django Implementation Standards

- Write clean, professional, maintainable code. Favor simple, explicit implementations over clever abstractions.
- Keep the codebase as simple and small as possible. Add only the files, dependencies, abstractions, settings, and patterns needed for the current requirement.
- Use descriptive names for models, views, forms, services, templates, CSS classes, and JavaScript modules.
- Keep functions and views focused. Split code when a function starts handling unrelated responsibilities.
- Avoid duplicated business logic. Reuse services/helpers where behavior is shared.
- Keep imports organized and remove unused code.
- Do not leave debug prints, commented-out experiments, temporary files, or TODOs without owner/context.
- Keep file structure professional and predictable. Add new files only where they clearly belong, and avoid dumping unrelated helpers into broad modules.
- Prefer small modules with clear responsibility over large mixed-purpose files.
- Avoid premature abstraction. Do not create generic frameworks, base classes, utility layers, or configuration systems until repeated real use makes them valuable.
- Keep naming consistent across models, forms, views, templates, URLs, tests, static assets, and frontend components.
- Do not introduce new frameworks, build tools, queues, storage systems, or frontend stacks without documenting why they are needed and updating this file.
- Keep app boundaries clear:
  - `accounts`: users, roles, host profiles, auth-related forms.
  - `village`: huts, cultural content, map structure, media references.
  - `simulations`: activity configs, quiz logic, progress, scores, badges, passport.
  - `bookings`: availability, reservations, booking status.
  - `marketplace`: products, carts, orders, reviews.
  - `dashboard`: role-specific screens and summaries.
  - `core`: home page, shared pages, common utilities.
- Prefer Django class-based or function-based views consistently within each app; do not mix patterns without reason.
- Put reusable business logic in services/helpers, not in templates.
- Keep templates simple: presentation only, no complex business rules.
- Use Django forms for validation and CSRF protection.
- Add migrations for model changes and keep them committed.
- Add admin registrations for content that admins must manage.
- Use transactions for checkout, orders, bookings, score persistence, and badge awarding.
- Make role checks explicit and test them.

Expected structure for each Django app as it grows:

- `models.py` or `models/` for database models.
- `views.py` or `views/` for request handlers.
- `urls.py` for app routing.
- `forms.py` for Django forms.
- `services.py` or `services/` for business workflows.
- `selectors.py` or query helpers for reusable read/query logic when needed.
- `tests/` for app tests once tests exceed a single small file.
- `admin.py` for Django admin registration.
- `templates/<app_name>/` for app templates when using Django templates.

Do not create a complex folder structure before it is useful, but when complexity appears, split files deliberately and consistently.

## Frontend, UI, and UX Standards

AerUla should feel warm, trustworthy, cultural, and easy to use. It should not feel like a generic admin template.

- Current Django-template UI may use Bootstrap for layout and components, then add custom CSS for AerUla brand polish.
- If a Vercel frontend is introduced, build it as a polished, component-driven frontend rather than copying Django templates directly.
- Keep navigation simple: Home, Virtual Village, Marketplace, Dashboard, Login/Register.
- Use clear primary actions like `Enter Virtual Village`, `Continue Journey`, `Complete Hut`, `Add to Cart`, and `Book Experience`.
- Design mobile first. Every page must work on phone, tablet, and desktop.
- Use readable contrast, visible focus states, semantic headings, labels, alt text, and keyboard-friendly controls.
- Avoid cluttered pages. Use short sections, clear cards, and strong visual hierarchy.
- The virtual village should be visually engaging but lightweight. Use SVG/Canvas/HTML interactions before adding heavier graphics.
- Do not add 3D, VR, AR, or AI chatbot features unless explicitly requested; these are future backlog items.
- Marketplace and booking flows should feel connected to hut completion and cultural learning, not separate from the simulation.
- Keep visual design consistent: spacing, typography, color usage, button hierarchy, empty states, error states, and loading states should feel intentional.
- Do not ship rough placeholder UI for user-facing pages unless the task explicitly asks for scaffolding only.
- Prefer reusable frontend components for cards, forms, navigation, status badges, hut previews, product tiles, and dashboard summaries.

## Simulation Performance Standards

AerUla is simulation-heavy, so performance is a product requirement.

- Keep MVP simulations lightweight and browser-native: JavaScript, SVG, Canvas, and CSS before heavier rendering approaches.
- Optimize for mobile devices first. Interactions must remain responsive on normal phones, not only desktop machines.
- Avoid unnecessary animation loops. Use `requestAnimationFrame` only when continuous rendering is actually needed.
- Stop timers, listeners, observers, and animation loops when a simulation is completed, hidden, or unmounted.
- Keep simulation state small and serializable so progress can be validated and saved cleanly.
- Do not load large media files on initial page load unless they are needed immediately.
- Compress and properly size hut images, product images, audio, and future simulation assets.
- Use lazy loading for below-the-fold media and noncritical content.
- Avoid blocking the main thread with expensive calculations. If complex logic is introduced later, consider Web Workers.
- Preserve accessibility: simulations need keyboard-friendly alternatives or fallback controls where practical.
- Server endpoints that save progress, quiz scores, bookings, and orders must be efficient and avoid unnecessary queries.
- Watch database query count for dashboard, marketplace, and passport pages; use `select_related`, `prefetch_related`, pagination, and indexes where appropriate.

## Testing and Acceptance

Create tests for every meaningful change. Every feature, bug fix, permission rule, model behavior, form validation, API/view response, and simulation scoring path should have tests.

Coverage target is 100%. If true 100% cannot be reached for a specific change, document the exact reason in the final response and keep the uncovered code limited to unavoidable integration boundaries.

Prioritize:

- Authentication and role routing.
- Host/admin permissions.
- Hut completion and progress persistence.
- Quiz scoring and badge awarding.
- Booking status changes.
- Cart/order totals and stock behavior.
- Marketplace product visibility and approval status.
- Simulation validation, scoring, completion state, and anti-tampering server checks.
- CORS/CSRF behavior when frontend and backend are split between Vercel and AWS.
- Error states, empty states, and invalid form submissions.

Minimum acceptance before a PR or push:

- `manage.py check` passes.
- Full test suite passes.
- Coverage is measured and remains at 100%, unless an explicit exception is documented.
- Migrations are created and applied when models change.
- No secrets are staged.
- The home page and touched views load locally.
- UI changes are checked at mobile and desktop widths.
- `AGENTS.md` is updated when the change affects architecture, deployment, testing, performance, security, or project standards.

When a frontend test stack is added, include appropriate unit/component tests and end-to-end coverage for critical user journeys. Critical journeys include registration/login, entering the virtual village, completing a hut simulation, earning a badge, viewing the passport, browsing marketplace products, adding to cart, and booking an experience.

Recommended future testing tools:

- Django: built-in test runner or pytest-django.
- Coverage: coverage.py with branch coverage enabled.
- Frontend on Vercel/Next.js: Vitest or Jest plus React Testing Library.
- End-to-end: Playwright for browser journeys across desktop and mobile widths.

## Git Hygiene

- Keep commits focused and descriptive.
- Do not commit `.env`, local logs, virtual environments, media uploads, database dumps, or cache folders.
- Check staged files before committing:

```powershell
git status
git diff --cached
```

- If deployment config is added, document exactly how to run it and what AWS resources it expects.

## Current Known Notes

- The local virtual environment was created around a Python `ensurepip` issue; dependencies may have been installed into `.venv\Lib\site-packages` with `pip --target`.
- PowerShell script execution may require:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init_dev.ps1
```

- PostgreSQL is local for development. Production must use managed PostgreSQL such as Amazon RDS.
