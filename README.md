## unote

# uNote - FastAPI Note-Taking Backend

A RESTful API backend for a note-taking application built with FastAPI and MySQL.

## Features

- 🔐 User authentication with JWT tokens
- 📝 CRUD operations for notes
- 🔒 Secure password hashing
- 🗄️ MySQL database integration
- 📚 Swagger/OpenAPI documentation

## Tech Stack

- FastAPI
- MySQL
- SQLAlchemy ORM
- PyJWT
- Python 3.10+

## Project Structure

```
unote/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py         # Database operations
│   ├── auth.py         # Authentication logic
│   ├── config.py       # Settings management
│   ├── database.py     # Database connection
│   ├── deps.py         # Dependencies
│   ├── init_db.py      # Database initialization
│   └── setup_db.py     # First-time setup
└── requirements.txt
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd unote
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
MYSQL_USER=notes_user
MYSQL_PASSWORD=notes_pass
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=notesdb
SECRET_KEY=your-secret-key-here
```

4. Initialize database:
```bash
python -m app.setup_db
```

5. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /homepage/login` - Login and get access token
- `POST /signup` - Create new user account

### Notes
- `GET /homepage/notes` - List all notes for current user
- `POST /homepage/notes` - Create new note
- `GET /homepage/notes/{note_id}` - Get specific note
- `PUT /homepage/notes/{note_id}` - Update note
- `DELETE /homepage/notes/{note_id}` - Delete note

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Usage

1. Create a user:
```bash
curl -X POST "http://localhost:8000/signup" \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "secretpass"}'
```

2. Login and get token:
```bash
curl -X POST "http://localhost:8000/homepage/login" \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "secretpass"}'
```

3. Create a note (using token):
```bash
curl -X POST "http://localhost:8000/homepage/notes" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{"title": "My First Note", "content": "Hello World!"}'
```

## Development

- Run tests: `pytest`
- Format code: `black app/`
- Check types: `mypy app/`

## License

MIT License - See LICENSE file for details