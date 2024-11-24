import fastapi
import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List,Optional
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import uuid

from datetime import datetime

# Get the current date and time
current_datetime = datetime.now()

formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#db config
db_config = {'user' : 'root', 'password' : 'yokesh2002','host' : 'localhost','database':'task_management','cursorclass': pymysql.cursors.DictCursor}

#data validation
class Task(BaseModel):
    task_name : str
    task_description : Optional[str] = None
    due_date : Optional[str] = None
    status :  Optional[str] = 'pending'

@app.on_event("startup")
def startup_db_client():
    print("hi")
    app.state.conn = pymysql.connect(**db_config)

@app.on_event("shutdown")
def shutdown_db_client():
    print("destroying the connection... la la la")
    app.state.conn.close()

@app.get("/tasks/", response_model=List[dict])
def get_tasks():
    cursor = app.state.conn.cursor()
    cursor.execute("select * from task_management.task_data;")
    tasks = cursor.fetchall()
    cursor.close()
    return tasks

@app.post("/insert_task/", response_model=dict)
def create_task(task: Task):
    print(task)
    cursor = app.state.conn.cursor()
    task_id = int(''.join(filter(str.isdigit, str(uuid.uuid4()))))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"INSERT INTO task_management.task_data (task_id,task_name, task_description, created_at,due_date, status) VALUES (%s, %s,%s, %s, %s, %s)",
                   (task_id,task.task_name, task.task_description, formatted_datetime,task.due_date, task.status))
    app.state.conn.commit()
    cursor.close()
    return {'result' : task_id}

@app.put('/update_task/{task_id}', response_model=dict)
def update_task(task_id : int, task:Task):
    cursor = app.state.conn.cursor()
    cursor.execute(f"UPDATE task_management.task_data SET task_name=%s, task_description=%s, due_date=%s, status=%s WHERE task_id=%s",
                   (task.task_name, task.task_description, task.due_date, task.status, task_id))
    app.state.conn.commit()
    cursor.close()
    return {'result' : f'updated {task_id}'}


# insert_task(Task(task_name="task1", task_description="task1", due_date="2023-09-01", status="pending"))
@app.delete('/delete_task/{task_id}', response_model=dict)
def delete_task(task_id: int):
    cursor = app.state.conn.cursor()
    cursor.execute(f"DELETE FROM task_management.task_data WHERE task_id={task_id}")
    app.state.conn.commit()
    cursor.close()
    return {'result' : f'deleted {task_id}'}



@app.get("/test-db")
async def test_db():
    # Create a cursor and execute a simple query
    cursor = app.state.conn.cursor()
    cursor.execute("show databases")
    result = cursor.fetchall()
    cursor.close()
    return {"result": result}

# fun   

if __name__ == "__main__":
    # Start the application
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")









# conn.close()






