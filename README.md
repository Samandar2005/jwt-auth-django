# JWT Authentication with Django Rest Framework

This project implements a secure authentication system using Django Rest Framework and JSON Web Tokens (JWT).

## Features

- Custom User Model with extended fields
- JWT Authentication
- Email-based authentication
- Registration and Login functionality
- Token refresh mechanism
- Secure logout with token blacklisting
- Rate limiting for API endpoints
- CORS configuration for frontend integration

## Technologies

- Python 3.12+
- Django 5.2+
- Django Rest Framework
- SimpleJWT
- django-cors-headers

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Samandar2005/jwt-auth-django.git
cd jwt-auth-django
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file in the root directory:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/register/` - Register new user
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "secure_password",
    "password2": "secure_password",
    "first_name": "Test",
    "last_name": "User"
  }
  ```

- `POST /api/auth/token/` - Login and get tokens
  ```json
  {
    "email": "test@example.com",
    "password": "secure_password"
  }
  ```

- `POST /api/auth/token/refresh/` - Refresh access token
  ```json
  {
    "refresh": "your-refresh-token"
  }
  ```

- `POST /api/auth/logout/` - Logout and blacklist token
  ```json
  {
    "refresh": "your-refresh-token"
  }
  ```

### Response Format

Success login response:
```json
{
    "access": "your-access-token",
    "refresh": "your-refresh-token",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
}
```

## Security Features

- Custom user model with email authentication
- JWT token authentication
- Token refresh mechanism
- Token blacklisting on logout
- Rate limiting for API endpoints
- CORS configuration
- Password validation

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

[Samandar2005](https://github.com/Samandar2005)

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
