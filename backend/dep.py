from typing import  Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from bson.objectid import ObjectId
from jose import jwt
from pydantic import ValidationError
from database import userInfoProcess
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

userinfoProcess = userInfoProcess()

async def get_current_user(token: str = Depends(reuseable_oauth)) -> dict :
    try:
        # 提取 JWT Token Depends(reuseable_oauth)
        # 解码和验证 Token
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
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
    user = await userinfoProcess.find({"_id":ObjectId(sub)})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user