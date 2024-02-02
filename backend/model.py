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

class userInfo(BaseModel):
    # userId
    username : str = Field(..., description="The username of the user")
    password : SecretStr = Field(..., description="The password of the user")
    email : EmailStr = Field(..., description="The email of the user")

class fileInfo(BaseModel):
    # fileId
    filename : str = Field(..., description="The filename of the file")
    contentType : str = Field(..., description="The contentType of the file")
    size : int = Field(..., description="The size of the file")
    md5 : str = Field(..., description="The md5 of the file")
    content : str
    processGraph : str

class resultInfo(BaseModel):
    # resultId
    fileId: str
    content : str

class uploadInfo(BaseModel):
    # uploadId
    fileId: str
    userId: str
