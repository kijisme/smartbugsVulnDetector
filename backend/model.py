from pydantic import BaseModel
from bson.objectid import ObjectId

class userInfo(BaseModel):
    # userId
    username : str
    password : str

class fileInfo(BaseModel):
    # fileId
    filename : str
    contentType : str
    size : int
    md5 : str
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