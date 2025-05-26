from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "postgresql://examactivity1_user:U63x80VWRvu2Y757nr8Ir20cGXmHgB0Q@dpg-d0q3gdeuk2gs73a6ttmg-a.oregon-postgres.render.com/examactivity1"
engine = create_engine(DATABASE_URL, client_encoding='utf8')
connection = engine.connect()

# FastAPI app setup
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    task: str
    deadline: str
    user: str

# Endpoints

@app.post("/login/")
async def user_login(user: User):
    result = connection.execute(
        text("SELECT * FROM users WHERE username = :username AND password = :password"),
        {"username": user.username, "password": user.password}
    ).fetchone()

    if result:
        return {"status": "Logged in"}
    return {"status": "Invalid credentials"}


@app.post("/create_user/")
async def create_user(user: User):
    check = connection.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()

    if check:
        return {"status": "User already exists"}

    connection.execute(
        text("INSERT INTO users (username, password) VALUES (:username, :password)"),
        {"username": user.username, "password": user.password}
    )
    connection.commit()
    return {"status": "User Created"}


@app.post("/create_task/")
async def create_task(task: Task):
    # Make sure the user exists
    user_check = connection.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": task.user}
    ).fetchone()

    if not user_check:
        return {"status": "User does not exist"}

    connection.execute(
        text("INSERT INTO tasks (task, deadline, username) VALUES (:task, :deadline, :username)"),
        {"task": task.task, "deadline": task.deadline, "username": task.user}
    )
    connection.commit()
    return {"status": "Task Created"}


@app.get("/get_tasks/")
async def get_tasks(name: str):
    result = connection.execute(
        text("SELECT task, deadline FROM tasks WHERE username = :username"),
        {"username": name}
    )

    task_list = [[row.task, row.deadline] for row in result]
    return {"tasks": task_list}
