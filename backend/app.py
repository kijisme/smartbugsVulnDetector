from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import UserInfo
from database import (
    fetch_one_user_info, 
    create_user_info, 
    update_user_info, 
    delete_user_info,
    )

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/api/UserInfo{username}", response_model=UserInfo)
async def get_todo_by_id(username):
    response = await fetch_one_user_info(username)
    if response:
        return response
    raise HTTPException(404, "fetch")

@app.post("/api/UserInfo", response_model=UserInfo)
async def post_todo(userInfo:UserInfo):
    response = await create_user_info(userInfo.dict())
    if response:
        return response
    raise HTTPException(404, "create")

@app.put("/api/UserInfo{username}", response_model=UserInfo)
async def put_todo(username, data:dict):
    response = await update_user_info(username, data)
    if response:
        return response
    raise HTTPException(404, "update")

@app.delete("/api/UserInfo/{username}")
async def delete_todo(username) :
    response = await delete_user_info(username)
    if response:
        return "success"
    raise HTTPException(404, "delete")