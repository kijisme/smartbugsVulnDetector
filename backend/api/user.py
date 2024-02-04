from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from model import userInfo, userAuth, ResponseModel
from database import userInfoProcess
from utils import bcryptEncrypt, create_access_token, create_refresh_token
from bson.objectid import ObjectId
from dep import get_current_user
# 初始化路由
router = APIRouter()
# 初始化加密器
encrypt = bcryptEncrypt()
# 初始化数据库驱动
userinfoProcess = userInfoProcess()

@router.post("/register", tags=["注册接口"])
async def register(userinfo: userInfo = Body(...)) -> ResponseModel:
    # 检查账户是否存在
    response = await userinfoProcess.find({'username':userinfo.username, 'email':userinfo.email})
    if response is None:
        # 加密密码
        password = encrypt.get_hashed_password(userinfo.password)
        # 添加账户
        response = await userinfoProcess.add({'username':userinfo.username, 'email':userinfo.email, 'password':password})

        return ResponseModel(response, True, "注册成功")
    raise HTTPException(status_code=400, detail="该用户已经注册")


@router.post("/login", tags=["登录接口"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:

    response = await userinfoProcess.find({'_id': ObjectId(form_data.username)})
    hashed_pass = response['password']
    if encrypt.verify_password(form_data.password, hashed_pass):
        # 使用用户id生成token
        tokeninfo = {
            "access_token": create_access_token(response['_id']),
            "refresh_token": create_refresh_token(response['_id']),
        }
        return {"access_token": create_access_token(response['_id']), "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")
