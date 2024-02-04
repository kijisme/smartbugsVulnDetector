from pydantic import BaseModel, EmailStr, Field

def ResponseModel(data, success, message):
    return {
        "data": [data],
        "success": success,
        "message": message,
    }

# 注册
class userInfo(BaseModel):
    username : str = Field(..., description="The username of the user")
    password : str = Field(..., description="The password of the user")
    email : EmailStr = Field(..., description="The email of the user")

# 登录
class userAuth(BaseModel):
    id : str = Field(..., description="The id of the user")
    password : str = Field(..., description="The password of the user")

class detectInfo(BaseModel):
    fileId : str = Field(..., description="The id of the file")