from motor.motor_asyncio import AsyncIOMotorClient
from model import userInfo, fileInfo, resultInfo, uploadInfo
from bson.objectid import ObjectId

class baseProcess(object):
    def __init__(self):
        self.CONNECT_STRING = 'mongodb://webAppUser:webAppPassword@localhost/smartbugsVulnDetector'
        # 获得连接客户端
        self.client = AsyncIOMotorClient(self.CONNECT_STRING)
        # 获得数据库
        self.database = self.client.smartbugsVulnDetector
    def helper(self, document)-> dict:

        return {k: str(document[k]) if k == '_id' else document[k] for k in document}


# userinfo
class userInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.userInfo

    async def add(self, info:dict) -> dict:
        insertRe = await self.collection.insert_one(info)
        document = await self.collection.find_one({"_id": insertRe.inserted_id})
        return self.helper(document)

    async def find(self, _id:str) -> dict:
        document = await self.collection.find_one({'id':ObjectId(_id)})
        if document:
        return self.helper(document)
    
    # async def update(self, _id, updateInfo):
    #     await self.collection.update_one({'_id':_id}, {'$set': updateInfo})
    #     document = await self.collection.find_one({'_id':_id})
    #     return document

# fileInfo
class fileInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.fileInfo

    async def add(self, info):
        document = info
        result = await self.collection.insert_one(document)
        return document

    async def find(self, _id):
        _id = ObjectId(_id)
        print(_id)
        document = await self.collection.find_one({'_id':_id})
        return document
    
    async def delete(self, _id):
        await self.collection.delete_one({'_id':u_idername})
        return True

# resultInfo
class resultInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.resultInfo

    async def add(self, info):
        document = info
        result = await self.collection.insert_one(document)
        return document

    async def find(self, _id):
        document = await self.collection.find_one({'_id':_id})
        return document
    
    async def delete(self, _id):
        await self.collection.delete_one({'_id':u_idername})
        return True

# uploadInfo
class uploadInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.uploadInfo

    async def add(self, info):
        document = info
        result = await self.collection.insert_one(document)
        return document

    async def find(self, _id):
        document = await self.collection.find_one({'_id':_id})
        return document
    
    async def delete(self, _id):
        await self.collection.delete_one({'_id':u_idername})
        return True


# # 查询
# async def fetch_one_user_info(username):
#     document = await collection.find_one({'username':username})
#     return document

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