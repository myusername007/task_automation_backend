# Task Automation

## Project overview
Task Automation Backend — REST API service for managing user tasks
with background execution support.

The system provides JWT-based authentication, role-based access control,
task execution history, and administrative monitoring capabilities.

Built with FastAPI, PostgreSQL, SQLAlchemy 2.x, and Docker.


### Features

- JWT authentication
- Role-based access (admin/user)
- Task CRUD
- Background execution
- TaskRun history
- Pagination & filtering
- Alembic migrations
- Dockerized setup

### Tech stack

- Python 3.11
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Docker

### Quickstart

`docker-compose up --build`

Swagger: `http://localhost:8000/docs`

### Environment variables
```
| Variable | Description |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection string |
| SECRET_KEY | JWT signing secret |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token lifetime in minutes |

```

### Typical API flow

1. Register a new user via `/auth/register`
2. Login via `/auth/login`
3. Authorize using Bearer token in Swagger
4. Create task via `/tasks`
5. Start execution via `/tasks/{id}/start`
6. Monitor status and runs history


### Admin access

Users with `is_admin = True` have access to:

- `GET /admin/tasks` — view all tasks
- `GET /admin/tasks/{id}/runs` — view execution history


### Background processing

Task execution is simulated using FastAPI BackgroundTasks.

When `/tasks/{id}/start` is called:

- A TaskRun record is created (status = pending)
- Background job updates status to running
- On completion, task status becomes done or failed
- Execution result is stored in the task record


### Migrations
```
docker-compose exec api alembic upgrade head
```


