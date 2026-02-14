## Project overview
Task automation backend - REST API for background tasks manage. 
Supports authentication with JWT, user roles, task runs history and admin access.
Implemented on FastAPI + PostgreSQL + Docker.

## Features
'''
- JWT authentication

- Role-based access (admin / user)

- Task CRUD

- Background execution

- TaskRun history

- Pagination & filtering

- Alembic migrations

- Dockerized setup
'''

## Tech stack
'''
- Python 3.11

- FastAPI

- SQLAlchemy 2.x

- PostgreSQL

- Alembic

- Docker

## Quickstart
'''
docker-compose up --build

Swagger:
http://localhost:8000/docs
'''

## Environment variables
'''
DATABASE_URL for access to database

SECRET_KEY for password hash

ACCESS_TOKEN_EXPIRE_MINUTES for JWT
'''

## API Flow
'''
1. Register

2. Login

3. Authorize

4. Create task

5. Start task

6. Check runs
'''

## Admin access
'''
is_admin = True
endpoints /admin/...

## Background processing
'''
POST /task/{id}/start
TaskRun created
background job updates status
'''

## Migrations
'''
docker-compose exec api alembic upgrade head
'''


