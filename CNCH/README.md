# CNCH

A Django REST API for managing school groups, students, content, and grading.

## Tech Stack

- **Python** 3.12
- **Django** 5.x + Django REST Framework
- **Authentication** — JWT (Simple JWT)
- **Package manager** — [uv](https://docs.astral.sh/uv/)
- **Production server** — Gunicorn
- **Static files** — WhiteNoise

## Project Structure

```
CNCH/
├── account/        # Users, school groups, students
├── content/        # Content management
├── grading/        # Grading system
├── mainproject/    # Django settings, root URLs
├── static/         # Source static files
├── staticfiles/    # Collected static files (generated, not committed)
├── templates/      # HTML templates
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Running with Docker (recommended)

### 1. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:

```ini
SECRET_KEY=<generate with the command below>
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Build and start

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

### 3. Run database migrations

On first run (or after model changes), apply migrations:

```bash
docker compose exec web python manage.py migrate
```

### 4. Create an admin user (optional)

```bash
docker compose exec web python manage.py createsuperuser
```

Admin panel: `http://localhost:8000/admin`

---

## Running locally (without Docker)

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setup

```bash
# Install dependencies
uv sync

# Copy and configure environment
cp .env.example .env

# Apply migrations
uv run python manage.py migrate

# Start the development server
uv run python manage.py runserver
```

---

## API Documentation

Base URL: `http://localhost:8000`

See [APIs.md](APIs.md) for full request/response examples.

### Endpoints

| Method | Endpoint               | Description                    |
|--------|------------------------|--------------------------------|
| POST   | `/user/groups/`        | Create a school group          |
| GET    | `/user/groups/{id}/`   | Group dashboard + students     |
| POST   | `/user/students/`      | Register a student             |
| PATCH  | `/user/students/{id}/` | Update student info            |

> Each school group can have a maximum of **6 students**.

### Authentication

The API uses JWT. Obtain tokens via the auth endpoints and pass the access token as a Bearer header:

```
Authorization: Bearer <access_token>
```

---

## Environment Variables

| Variable        | Description                                   | Default                     |
|-----------------|-----------------------------------------------|-----------------------------|
| `SECRET_KEY`    | Django secret key                             | insecure default (dev only) |
| `DEBUG`         | Enable debug mode                             | `False`                     |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames/IPs | `localhost,127.0.0.1`       |
