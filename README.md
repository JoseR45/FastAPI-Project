# FastAPI Project

## Installation and Execution

### 1. Clone the Repository

### 2. Create the `.env` File
Create a `.env` file in the root directory with the following content:

```ini
SECRET_KEY=JWT_key_example
ALGORITHM=HS256

POSTGRES_DB=fastapi_db
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=fastapi_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

APP_PORT=8000
```

### 3. Start the Containers
```bash
docker-compose up -d
```

### 4. Run the `admin_user.py` Script
```bash
docker exec -it fastapi_container python3 admin_user.py
```


