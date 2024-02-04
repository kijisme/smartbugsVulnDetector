from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from model import userInfo, ResponseModel
from utils import bcryptEncrypt, create_access_token, create_refresh_token
from bson.objectid import ObjectId
from dep import get_current_user

from datetime import datetime, timedelta
from jose import jwt

from api.common import userinfoProcess
from dep import reuseable_oauth
from utils import (
    ALGORITHM,
    JWT_REFRESH_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)

# 初始化路由
router = APIRouter()
# 初始化加密器
encrypt = bcryptEncrypt()

@router.post("/register", tags=["注册接口"])
async def register(userinfo: userInfo = Body(...)) -> ResponseModel:
    # 检查账户是否存在
    response = await userinfoProcess.find({'username':userinfo.username, 'email':userinfo.email})
    if response is None:
        # 加密密码
        password = encrypt.get_hashed_password(userinfo.password)
        # 添加账户
        response = await userinfoProcess.add({'username':userinfo.username, 'email':userinfo.email, 'password':password})

        return ResponseModel(response, True, "/register")
    raise HTTPException(status_code=400, detail="该用户已经注册")

@router.post("/login", tags=["登录接口"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:

    response = await userinfoProcess.find({'_id': ObjectId(form_data.username)})
    if response is not None:
        hashed_pass = response['password']
        if encrypt.verify_password(form_data.password, hashed_pass):
            # 使用用户id生成token
            tokeninfo = {
                "access_token": create_access_token(response['_id']),
                "refresh_token": create_refresh_token(response['_id']),
                "token_type": "bearer",
            }
            return tokeninfo
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    raise HTTPException(status_code=400, detail="Invalid username")

# 刷新令牌
@router.post("/refreshtoken", tags=["刷新令牌"])
async def refresh_token(userinfo: dict = Depends(get_current_user), refresh_token: str = Depends(reuseable_oauth)) -> ResponseModel:
    try:
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload['exp']
        sub = payload['sub']
        # 检测token是否过期
        if datetime.fromtimestamp(exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 获取用户信息 sub
    if sub != userinfo['_id']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    # 创建新的访问令牌
    access_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token({"sub": sub}, expires_delta=access_token_expires)
    
    # 返回新的访问令牌
    return ResponseModel({'new_access_token':new_access_token}, True, '/refreshtoken')