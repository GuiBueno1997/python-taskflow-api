# TaskFlow API

A RESTful Task Management API built with Python, FastAPI, SQLAlchemy, and PostgreSQL.

TaskFlow API is a backend portfolio project focused on learning and implementing RESTful API development, database integration, and CRUD operations using Python.

## Technologies

- **Python 3.10**
- **FastAPI** – REST API framework
- **Uvicorn** – ASGI server
- **SQLAlchemy 2.0** – Object-relational mapper (ORM)
- **PostgreSQL** – Relational database
- **Psycopg 3** – PostgreSQL database adapter
- **Pydantic** – Data validation
- **Postman** – API testing
- **Git and GitHub** – Version control

## Features

- Create tasks.
- Retrieve all tasks.
- Retrieve a specific task by ID.
- Filter tasks by completion status.
- Limit the number of returned tasks.
- Update tasks using PUT.
- Partially update tasks using PATCH.
- Delete tasks.
- PostgreSQL database integration through SQLAlchemy.
- Environment variable configuration using python-dotenv.
- Interactive API documentation through Swagger UI.
- Postman collection with automated response checks.

## Project Structure

```text
TaskFlow_API/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── init_db.py
│
├── scripts/
│   ├── __init__.py
│   ├── create_task.py
│   ├── read_tasks.py
│   ├── update_task.py
│   └── delete_task.py
│
├── tests/
│
├── postman/
│   ├── collections/
│   └── environments/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Database Configuration

TaskFlow API uses PostgreSQL as its database and SQLAlchemy to manage database interactions.

Create a PostgreSQL database named:

```sql
CREATE DATABASE taskflow_db;
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/taskflow_db
```

Replace `username` and `password` with your PostgreSQL credentials.

**Important:** Never commit your actual `.env` file or database credentials to GitHub.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/GuiBueno1997/python-taskflow-api.git
cd python-taskflow-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create your `.env` file using the database configuration described above.

### 5. Initialize the database tables

```bash
python -m app.init_db
```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint                                   | Description                             |
| ------ | ------------------------------------------ | --------------------------------------- |
| GET    | `/`                                      | API welcome message                     |
| GET    | `/health`                                | Health check                            |
| POST   | `/tasks`                                 | Create a task                           |
| GET    | `/tasks`                                 | Retrieve all tasks                      |
| GET    | `/tasks/{task_id}`                       | Retrieve a specific task                |
| PUT    | `/tasks/{task_id}`                       | Replace a task                          |
| PATCH  | `/tasks/{task_id}`                       | Partially update a task                 |
| DELETE | `/tasks/{task_id}`                       | Delete a task                           |
| GET    | `/tasks/{task_id}/subtasks`              | Subtasks demonstration endpoint         |
| GET    | `/tasks/{task_id}/subtasks/{subtask_id}` | Specific subtask demonstration endpoint |

### Query Parameters

The task listing endpoint supports:

- `completed`: Filter tasks by completion status (`true` or `false`).
- `limit`: Maximum number of tasks returned (default: 10, maximum: 100).

Example:

```http
GET /tasks?completed=false&limit=5
```

### Create Task Example

**Request:**

```http
POST /tasks
Content-Type: application/json
```

**JSON Body:**

```json
{
    "title": "Learn FastAPI",
    "description": "Build a RESTful API with Python",
    "completed": false
}
```

## Postman Collection

The project includes a Postman collection for manually testing the API endpoints and validating HTTP responses.

The collection includes requests for:

- Create Task
- List Tasks
- Get Task
- PUT Update
- PATCH Partial Update
- Delete Task

The Postman environment uses variables such as `base_url` and `task_id` to simplify request configuration and testing.

## SQLAlchemy Scripts

The `scripts/` directory contains standalone Python scripts demonstrating database CRUD operations directly through SQLAlchemy:

- `create_task.py`
- `read_tasks.py`
- `update_task.py`
- `delete_task.py`

Run them from the project root:

```bash
python -m scripts.create_task
python -m scripts.read_tasks
python -m scripts.update_task
python -m scripts.delete_task
```

These scripts are intended for database learning and experimentation.

## Testing

The project includes automated tests using Pytest and FastAPI TestClient.

Tests run against an isolated in-memory SQLite database, ensuring that the development PostgreSQL database is not modified during test execution.

### Run automated tests

```bash
python -m pytest -v
```

### Run tests with coverage

```bash
python -m pytest --cov=app --cov-report=term-missing
```

### Test coverage

The test suite currently includes 19 automated tests covering:

- API health checks and root endpoint
- Task creation, retrieval, updating and deletion
- Partial task updates
- Task filtering and result limits
- HTTP error handling (404 and 422)
- Subtask demonstration endpoints

Current coverage:

- 100% coverage in `app/main.py`
- 100% coverage in `app/models.py`
- 92% overall application coverage

## Current Limitations

- Subtask endpoints currently return demonstration responses and are not connected to persistent database models.
- Automated tests currently use an in-memory SQLite database; integration tests against PostgreSQL are not yet configured.
- Database schema migrations are not yet configured.

## Future Improvements

- Add Alembic for database migrations.
- Implement persistent subtasks and relationships.
- Add authentication and authorization.
- Improve API response schemas and validation.
- Introduce pagination.
- Apply additional software architecture and design patterns.

## Author

**Guilherme Bueno**

GitHub: [GuiBueno1997](https://github.com/GuiBueno1997)
