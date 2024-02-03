from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from model import userInfo, ResponseModel, ErrorResponseModel, userAuth
from database import userInfoProcess
from utils import bcryptEncrypt, create_access_token, create_refresh_token
from bson.objectid import ObjectId
# 初始化路由
router = APIRouter()
# 初始化加密器
encrypt = bcryptEncrypt()
# 初始化数据库驱动
userinfoProcess = userInfoProcess()

@router.post("/register", tags=["注册接口"])
async def register(userinfo:userInfo = Body(...)):
    userinfo = jsonable_encoder(userinfo)
    findUser = {'username':userinfo['username'], 'email':userinfo['email']}
    # 检查账户是否存在
    response = await userinfoProcess.find(findUser)
    if response is not None:
        return ErrorResponseModel("error", 404, "该账户名或email已注册")

    # 加密密码
    userinfo['password'] = encrypt.get_hashed_password(userinfo['password'])
    # 添加账户
    response = await userinfoProcess.add(userinfo)

    return ResponseModel(response, "注册成功")


@router.post("/login", tags=["登录接口"])
async def login(form_data: userAuth = Depends()):

    response = await userinfoProcess.find({'_id': ObjectId(form_data.id), 'username':form_data.username})
    if response:
        hashed_pass = response['password']
        if encrypt.verify_password(form_data.password, hashed_pass):
            tokeninfo = {
                "access_token": create_access_token(response['email']),
                "refresh_token": create_refresh_token(response['email']),
            }
            return ResponseModel(tokeninfo, "登录成功")
        return ErrorResponseModel("error.", 404, "账号或密码错误")
    return ErrorResponseModel("error.", 404, "不存在该用户")

