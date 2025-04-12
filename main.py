from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import csv
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # This allows all headers
)

USERS_FILE = "data/users.csv"
TASKS_FILE = "data/tasks.csv"

class User(BaseModel):
    username: str
    password: str 

class Task(BaseModel):
    task: str
    deadline: str 
    user: str

@app.post("/login/")
async def user_login(user: User):
    df = pd.read_csv(USERS_FILE)
    if len(df[df["username"] == user.username]):
        return {"status": "Logged in"}

@app.post("/create_user/")
async def create_user(user: User):
    df = pd.read_csv(USERS_FILE)
    df.loc[len(df)] = [user.username, user.password]
    df.to_csv(USERS_FILE, index = False)
    return {"status": "User Created"}

@app.post("/create_task/")
async def create_task(task: Task):
    df = pd.read_csv(TASKS_FILE)
    df.loc[len(df)] = [task.task, task.deadline, task.user]
    df.to_csv(TASKS_FILE, index = False)    
    return {"status": "Task Created"}

@app.get("/get_tasks/")
async def get_tasks(name: str):
    df = pd.read_csv(TASKS_FILE)
    df = df[df["user"] == name]
    task_list = []
    for _, row in df.iterrows():
        task_list.append([row.task, row.deadline, row.user])
    
    return {"tasks": [task_list]}