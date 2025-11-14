# JWT Authentication with Django Rest Framework

This project implements a secure authentication system using Django Rest Framework and JSON Web Tokens (JWT).

## Features

- Custom User Model with extended fields (phone, avatar, bio, birth_date)
- CustomUserManager for proper user creation and superuser management
- CustomUserAdmin for enhanced Django admin interface
- JWT Authentication with email-based login
- Registration and Login functionality
- Token refresh mechanism
- Secure logout with token blacklisting
- Rate limiting for API endpoints
- CORS configuration for frontend integration
- Interactive API documentation (Swagger/ReDoc)
- Production-ready security settings
- Comprehensive test coverage
- Environment-based configuration

## Technologies

- Python 3.12+
- Django 5.2+
- Django Rest Framework
- SimpleJWT
- django-cors-headers
- drf-yasg (Swagger/OpenAPI)
- PostgreSQL (production)
- Nginx + Gunicorn (deployment)
- Redis (optional caching)

## User Model Architecture

### CustomUserManager

The project includes a custom user manager (`CustomUserManager`) that extends Django's `BaseUserManager`. This is essential for proper functionality when using email as the primary authentication field:

- **Why it's needed**: When `USERNAME_FIELD` is set to `email`, Django's default user manager doesn't properly handle `createsuperuser` and other authentication functions. The custom manager ensures:
  - Proper user creation with email normalization
  - Correct superuser creation with all required permissions
  - Validation of required fields (email and username)

- **Methods**:
  - `create_user()`: Creates a regular user with email and password
  - `create_superuser()`: Creates a superuser with staff and superuser permissions

### CustomUserAdmin

The Django admin interface is configured with `CustomUserAdmin` which extends Django's default `UserAdmin`:

- **Features**:
  - Email-based user management
  - Display of custom fields (phone, bio, avatar, birth_date)
  - Enhanced search functionality (email, username, first_name, last_name)
  - Filtering by staff status, active status, and date joined
  - Proper field organization in admin forms
  - Read-only fields for important dates (date_joined, last_login)

- **Access**: Navigate to `/admin/` after creating a superuser to manage users through the admin interface.

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
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings (optional for production)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# JWT settings
ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=7

# Email settings (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Security settings
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
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

## API Documentation

The API documentation is available through Swagger UI and ReDoc interfaces:

- Swagger UI: `/swagger/` - Interactive API documentation
- ReDoc: `/redoc/` - Alternative API documentation
- JSON format: `/swagger.json` - Raw API specification

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

## Deployment

### Prerequisites

- Python 3.12+
- PostgreSQL (recommended for production)
- Nginx
- Domain name (optional)
- SSL certificate (recommended)

### Production Setup

1. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
```

2. Create PostgreSQL database:
```sql
sudo -u postgres psql
CREATE DATABASE jwt_auth_db;
CREATE USER jwt_auth_user WITH PASSWORD 'your_secure_password';
ALTER ROLE jwt_auth_user SET client_encoding TO 'utf8';
ALTER ROLE jwt_auth_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE jwt_auth_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE jwt_auth_db TO jwt_auth_user;
\q
```

3. Clone and setup the project:
```bash
git clone https://github.com/Samandar2005/jwt-auth-django.git
cd jwt-auth-django
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

4. Create production environment variables:
```bash
# Create and edit .env file
nano .env
```

Add the following environment variables:
```env
DJANGO_SECRET_KEY=your-very-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
DATABASE_URL=postgresql://jwt_auth_user:your_secure_password@localhost:5432/jwt_auth_db
```

5. Setup database and static files:
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

6. Create systemd service:
```bash
sudo nano /etc/systemd/system/jwt-auth.service
```

Add the following content:
```ini
[Unit]
Description=JWT Auth Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/jwt-auth-django
ExecStart=/path/to/jwt-auth-django/.venv/bin/gunicorn core.wsgi:application --workers 3 --bind unix:/run/jwt-auth.sock
Restart=always

[Install]
WantedBy=multi-user.target
```

7. Configure Nginx:
```bash
sudo nano /etc/nginx/sites-available/jwt-auth
```

Add the following configuration:
```nginx
server {
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/jwt-auth-django;
    }

    location /media/ {
        root /path/to/jwt-auth-django;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/jwt-auth.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}

server {
    if ($host = www.your-domain.com) {
        return 301 https://$host$request_uri;
    }

    if ($host = your-domain.com) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 404;
}
```

8. Enable and start services:
```bash
sudo ln -s /etc/nginx/sites-available/jwt-auth /etc/nginx/sites-enabled
sudo systemctl start jwt-auth
sudo systemctl enable jwt-auth
sudo systemctl restart nginx
```

### SSL Certificate (Let's Encrypt)

1. Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. Get SSL certificate:
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Security Recommendations

1. Regular Updates:
```bash
sudo apt update && sudo apt upgrade
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

2. Backup Database:
```bash
pg_dump jwt_auth_db > backup_$(date +%Y%m%d).sql
```

3. Monitor Logs:
```bash
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
journalctl -u jwt-auth
```

### Performance Optimization

1. Enable Gzip compression in Nginx:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 10240;
gzip_proxied expired no-cache no-store private auth;
gzip_types text/plain text/css text/xml text/javascript application/json application/x-javascript application/xml;
```

2. Cache settings in Django:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

3. Database optimization:
```sql
VACUUM ANALYZE;
```

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
