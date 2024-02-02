from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware

from model import userInfo, fileInfo, resultInfo, uploadInfo, ResponseModel
from database import userInfoProcess, fileInfoProcess, resultInfoProcess, uploadInfoProcess

# 初始化app
app = FastAPI()
# 初始化数据库驱动
userinfoProcess = userInfoProcess()
fileinfoProcess = fileInfoProcess()
resultinfoProcess = resultInfoProcess()
uploadinfoProcess = uploadInfoProcess()

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

@app.get("/", tags=["向导页面"])
async def read_root():
    return {"message": "智能合约漏洞监测系统"}


@app.post("/register", tags=["注册接口"])
async def register(userinfo:userInfo = Body(...)):
    userinfo = jsonable_encoder(userinfo)
    response = await userinfoProcess.add(userinfo)
    return ResponseModel(response, "注册成功")

@app.post("/login", tags=["登录接口"])
async def login(_id, username, password):

    response = await userinfoProcess.find(_id)
    if response:
        if response['password'] != password:
            return ResponseModel('[]', "密码或账户名称错误")
        return ResponseModel(response, "登录成功")
    return ErrorResponseModel("出错了.", 404, "不存在该用户id")


# @app.get("/api/UserInfo{username}", response_model=UserInfo)
# async def get_todo_by_id(username):
#     response = await fetch_one_user_info(username)
#     if response:
#         return response
#     raise HTTPException(404, "fetch")

# @app.post("/api/UserInfo", response_model=UserInfo)
# async def post_todo(userInfo:UserInfo):
#     response = await create_user_info(userInfo.dict())
#     if response:
#         return response
#     raise HTTPException(404, "create")

# @app.put("/api/UserInfo{username}", response_model=UserInfo)
# async def put_todo(username, data:dict):
#     response = await update_user_info(username, data)
#     if response:
#         return response
#     raise HTTPException(404, "update")

# @app.delete("/api/UserInfo/{username}")
# async def delete_todo(username) :
#     response = await delete_user_info(username)
#     if response:
#         return "success"
#     raise HTTPException(404, "delete")