from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

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
    
    async def find(self, info:dict):
        document = await self.collection.find_one(info)
        if document:
            return self.helper(document)

# uploadInfo
class uploadInfoProcess(baseProcess):
    def __init__(self):
        super().__init__()
        self.collection = self.database.uploadInfo

    async def add(self, info:dict) -> dict:
        insertRe = await self.collection.insert_one(info)
        document = await self.collection.find_one({"_id": insertRe.inserted_id})
        return self.helper(document)

    async def find(self, info:dict):
        document = await self.collection.find_one(info)
        if document:
            return self.helper(document)
    
    async def update(self, filter:dict, info:dict) -> dict:
        # 查询是否满足唯一
        if '_id' in filter or await self.collection.count_documents(filter) == 1:
            updateRe = await self.collection.update_one(filter, {"$set": info}, upsert=True)
            # document = await self.collection.find_one({"_id": updateRe.upserted_id})
            return updateRe.raw_result  
    
    async def find_all(self, filter:dict) -> dict:
        documents =  self.collection.find(filter)
        if documents:
            documents_list = [] 
            async for document in documents:
                documents_list.append(self.helper(document))
            return documents_list
    
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
        if document:
            return self.helper(document)
    
