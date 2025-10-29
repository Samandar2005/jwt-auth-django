# jwt-auth-django

Simple JWT authentication example with Django REST Framework.

## Endpoints

- POST /api/auth/register/  -> register new user
- POST /api/auth/token/     -> obtain access & refresh
- POST /api/auth/token/refresh/ -> refresh access
- POST /api/auth/logout/    -> blacklist refresh (requires Authorization header)

## Setup

1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver
