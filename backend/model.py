from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, SecretStr, EmailStr, Field

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

# 登录
class userAuth(BaseModel):
    id : str = Field(..., description="The id of the user")
    username : str = Field(..., description="The username of the user")
    password : str = Field(..., description="The password of the user")

# 注册
class userInfo(BaseModel):
    username : str = Field(..., description="The username of the user")
    password : str = Field(..., description="The password of the user")
    email : EmailStr = Field(..., description="The email of the user")

# 验证
class tokenInfo(BaseModel):
    access_token: str
    token_type: str


# 检测
class detectInfo(BaseModel):
    fileId : str = Field(..., description="The id of the file")
    contentType : str  = Field(..., description="The content_type of the file")

# class fileInfo(BaseModel):
#     # fileId
#     filename : str = Field(..., description="The filename of the file")
#     size : int = Field(..., description="The size of the file")
#     content : str
#     processGraph : str

# class resultInfo(BaseModel):
#     # resultId
#     fileId: str
#     content : str

# class uploadInfo(BaseModel):
#     # uploadId
#     fileId: str
#     userId: str
