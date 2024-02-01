from model import UserInfo
from motor.motor_asyncio import AsyncIOMotorClient

CONNECT_STRING = 'mongodb://webAppUser:webAppPassword@localhost/smartbugsVulnDetector'

# 获得连接客户端
client = AsyncIOMotorClient(CONNECT_STRING)
# 获得数据库
database = client.smartbugsVulnDetector
# 获得集合
collection = database.user_info
print(collection)
# 查询
async def fetch_one_user_info(username):
    document = await collection.find_one({'username':username})
    return document

# 添加
async def create_user_info(user_info):
    document = user_info
    result = await collection.insert_one(document)
    return document

# 更新
async def update_user_info(username, userInfo):
    await collection.update_one({'username':username}, {'$set': userInfo})
    document = await collection.find_one({'username':username})
    return document

# 删除
async def delete_user_info(username):
    await collection.delete_one({'username':username})
    return True