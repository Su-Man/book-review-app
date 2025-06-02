# Book Review RESTful Web Application

A sample backend project for demonstrating a complete DevOps pipeline with Jenkins.

## Features
- JWT-based user authentication (register/login)
- CRUD operations for book reviews
- Admin-only endpoints for user management
- API health check
- Unit/integration tests (pytest)
- Dockerized build and deployment

## Project Structure
- `app/` - Flask application code
- `tests/` - Pytest test cases
- `Dockerfile` - Containerization
- `Jenkinsfile` - CI/CD pipeline
- `sonar-project.properties` - SonarQube config

## Running Locally
```bash
pip install -r requirements.txt
export FLASK_APP=app
flask run
```

## Docker Build/Run
```bash
docker build -t bookreviewapp .
docker run -p 5000:5000 bookreviewapp
```

## Running Tests
```bash
pytest
```

## API Endpoints
- `POST /register` - Register new user
- `POST /login` - Login and get JWT
- `GET /reviews` - List reviews
- `POST /reviews` - Add review (JWT required)
- `PUT /reviews/<id>` - Update review (JWT required)
- `DELETE /reviews/<id>` - Delete review (JWT/admin required)
- `GET /admin/users` - List all users (admin only)
- `GET /health` - Health check
