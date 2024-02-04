from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from fastapi import HTTPException

class baseProcess(object):
    def __init__(self):
        self.CONNECT_STRING = 'mongodb://webAppUser:webAppPassword@localhost/smartbugsVulnDetector'
        # 获得连接客户端
        self.client = AsyncIOMotorClient(self.CONNECT_STRING)
        # 获得数据库
        self.database = self.client.smartbugsVulnDetector
    def helper(self, document)-> dict:
        return {k: str(document[k]) if isinstance(document[k], ObjectId) else document[k] for k in document}


# userinfo
class userInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.userInfo

    async def add(self, info:dict) -> dict:
        insertRe = await self.collection.insert_one(info)
        document = await self.collection.find_one({"_id": insertRe.inserted_id})
        return self.helper(document)

    async def find(self, info:dict) -> dict:
        document = await self.collection.find_one(info)
        if document:
            return self.helper(document)
    
# fileInfo
class fileInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.fileInfo

    async def add(self, info:dict) -> dict:
        insertRe = await self.collection.insert_one(info)
        document = await self.collection.find_one({"_id": insertRe.inserted_id})
        return self.helper(document)
    
    async def find(self, info:dict) -> dict:
        document = await self.collection.find_one(info)
        if document:
            return self.helper(document)
        raise HTTPException(status_code=404, detail="find error")


# uploadInfo
class uploadInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.uploadInfo

    async def add(self, info:dict) -> dict:
        insertRe = await self.collection.insert_one(info)
        document = await self.collection.find_one({"_id": insertRe.inserted_id})
        return self.helper(document)

    async def find(self, info:dict) -> dict:
        document = await self.collection.find_one(info)
        if document:
            return self.helper(document)
        raise HTTPException(status_code=404, detail="find error")
    
    async def update(self, filter:dict, info:dict) -> dict:
        # 查询是否满足唯一
        if '_id' in filter or await self.collection.count_documents(filter) == 1:
            updateRe = await self.collection.update_one(filter, {"$set": info}, upsert=True)
            # document = await self.collection.find_one({"_id": updateRe.upserted_id})
            return updateRe.raw_result
        raise HTTPException(status_code=404, detail="update error")    
    
    async def find_all(self, filter:dict) -> dict:
        document = await self.collection.find(filter)
        if document:
            return self.helper(document)
        raise HTTPException(status_code=404, detail="find error")

    
# resultInfo
class resultInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.resultInfo

    async def add(self, info:dict) -> dict:
        insertRe = await self.collection.insert_one(info)
        document = await self.collection.find_one({"_id": insertRe.inserted_id})
        return self.helper(document)

    async def find(self, info:dict) -> dict:
        document = await self.collection.find_one(info)
        print(self.helper(document))
        if document:
            return self.helper(document)
        raise HTTPException(status_code=404, detail="find error")
    




# # # 查询
# # async def fetch_one_user_info(username):
# #     document = await collection.find_one({'username':username})
# #     return document

# # 添加
# async def create_user_info(user_info):
#     document = user_info
#     result = await collection.insert_one(document)
#     return document

# # 更新
# async def update_user_info(username, userInfo):
#     await collection.update_one({'username':username}, {'$set': userInfo})
#     document = await collection.find_one({'username':username})
#     return document

# # 删除
# async def delete_user_info(username):
#     await collection.delete_one({'username':username})
#     return True