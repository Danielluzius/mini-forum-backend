# Django REST Framework - Mini Forum

A RESTful API for a simple forum application built with Django REST Framework, featuring user authentication, post and comment management, permissions, and advanced throttling.

## Features

- **User Authentication**: Token-based authentication with registration and login endpoints
- **Post Management**: Create, read, update, and delete forum posts
- **Comment System**: Add comments to posts with full CRUD operations
- **Permissions**: Owner-based permissions for editing and deleting content
- **API Throttling**: Rate limiting for anonymous users, authenticated users, and POST requests
- **Custom Throttle Class**: Specialized throttling that only affects POST requests (1 per minute)

## Tech Stack

- **Django 6.0.1**: High-level Python web framework
- **Django REST Framework 3.16.1**: Powerful toolkit for building Web APIs
- **SQLite**: Lightweight database for development
- **Token Authentication**: Built-in DRF authentication

## Project Structure

```
drf-mini-forum/
├── backend/
│   ├── core/                   # Project settings
│   ├── forum_app/              # Forum application
│   │   ├── api/                # API views, serializers, URLs
│   │   ├── models.py           # Post and Comment models
│   │   └── throttling.py       # Custom throttle classes
│   ├── user_auth_app/          # Authentication application
│   │   └── api/                # Registration and login endpoints
│   ├── db.sqlite3              # SQLite database
│   └── manage.py               # Django management script
```

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd drf-mini-forum
   ```

2. **Create and activate virtual environment**

   ```bash
   # Windows
   python -m venv backend\.venv
   backend\.venv\Scripts\activate

   # macOS/Linux
   python3 -m venv backend/.venv
   source backend/.venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## Configuration

### Throttling Settings

The API implements three levels of throttling configured in `backend/core/settings.py`:

```python
'DEFAULT_THROTTLE_RATES': {
    'anon': '100/hour',      # Anonymous users: 100 requests per hour
    'user': '1000/hour',     # Authenticated users: 1000 requests per hour
    'posts': '1/minute',     # POST requests only: 1 per minute
}
```

### Custom Throttle Class

Located in `backend/forum_app/throttling.py`:

```python
class PostThrottle(UserRateThrottle):
    scope = 'posts'

    def allow_request(self, request, view):
        # Only throttle POST requests
        if request.method != 'POST':
            return True
        return super().allow_request(request, view)
```

This ensures GET requests are not affected by the stricter POST throttling.

## API Endpoints

### Authentication

| Method | Endpoint          | Description         | Auth Required |
| ------ | ----------------- | ------------------- | ------------- |
| POST   | `/auth/register/` | Register new user   | No            |
| POST   | `/auth/login/`    | Login and get token | No            |

### Posts

| Method | Endpoint           | Description     | Auth Required |
| ------ | ------------------ | --------------- | ------------- |
| GET    | `/api/posts/`      | List all posts  | No            |
| GET    | `/api/posts/{id}/` | Get single post | No            |
| POST   | `/api/posts/`      | Create new post | Yes           |
| PUT    | `/api/posts/{id}/` | Update own post | Yes (Owner)   |
| DELETE | `/api/posts/{id}/` | Delete own post | Yes (Owner)   |

### Comments

| Method | Endpoint              | Description        | Auth Required |
| ------ | --------------------- | ------------------ | ------------- |
| GET    | `/api/comments/`      | List all comments  | No            |
| GET    | `/api/comments/{id}/` | Get single comment | No            |
| POST   | `/api/comments/`      | Create new comment | Yes           |
| PUT    | `/api/comments/{id}/` | Update own comment | Yes (Owner)   |
| DELETE | `/api/comments/{id}/` | Delete own comment | Yes (Owner)   |

## Usage Examples

### Register a User

```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "repeated_password": "securepass123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

Response:

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Create a Post

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post!"
  }'
```

### Get All Posts

```bash
curl http://localhost:8000/api/posts/
```

## Throttling Behavior

### Scenario 1: POST Request Throttling

```bash
# First POST - Success (201 Created)
curl -X POST http://localhost:8000/api/posts/ ...

# Second POST within 1 minute - Throttled (429 Too Many Requests)
curl -X POST http://localhost:8000/api/posts/ ...
```

Response:

```json
{
  "detail": "Request was throttled. Expected available in 45 seconds."
}
```

### Scenario 2: GET Requests Not Affected

```bash
# GET requests work fine even after POST is throttled
curl http://localhost:8000/api/posts/  # 200 OK
curl http://localhost:8000/api/posts/  # 200 OK
curl http://localhost:8000/api/posts/  # 200 OK
```

## Development

### Running Tests

```bash
python manage.py test
```

### Admin Interface

Access the Django admin at `http://localhost:8000/admin/` with superuser credentials.

### Database Management

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (caution: deletes all data)
rm db.sqlite3
python manage.py migrate
```

## Troubleshooting

### Issue: Token Authentication Not Working

**Solution**: Ensure the `Authorization` header format is correct:

```
Authorization: Token YOUR_TOKEN_HERE
```

### Issue: Throttling Too Strict for Testing

**Solution**: Temporarily increase limits in `settings.py`:

```python
'posts': '10/minute',  # Instead of '1/minute'
```

Remember to change it back for production!

### Issue: Permission Denied (403)

**Solution**: You can only edit/delete your own posts and comments. Ensure you're using the correct user token.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is for educational purposes as part of the Developer Academy Back-End Course.

## Acknowledgments

- Built as part of Module 8: DRF Authentication & Permissions
- Django REST Framework Documentation
- Developer Academy Back-End Course
