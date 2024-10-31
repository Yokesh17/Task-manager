import fastapi
import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List,Optional
from contextlib import asynccontextmanager
import logging 
from fastapi.middleware.cors import CORSMiddleware
import pymysql

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#db config
db_config = {'user' : 'root', 'password' : 'yokesh2002','host' : 'localhost','database':'task_management'}

#data validation    
class Task(BaseModel):
    task_name : str
    task_description : Optional[str] = None
    due_date : Optional[str] = None
    status :  Optional[str] = 'pending'


@asynccontextmanager
async def lifespan(app : FastAPI):
    print("started")
    logger.info("Connecting to the database...")
    app.state.conn = pymysql.connect(**db_config)
    yield
    app.state.conn.close()
    logger.info("Disconnected from the database.")


app.lifespan=lifespan

@app.get("/test-db")
async def test_db():
    if not hasattr(app.state, "conn"):
        raise HTTPException(status_code=500, detail="Database connection is not established.")
    
    # Create a cursor and execute a simple query
    cursor = app.state.conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchall()
    cursor.close()
    return {"result": result}



if __name__ == "__main__":
    # Start the application
    uvicorn.run(app, host="127.0.0.12", port=8000, log_level="info")








# conn.close()






