from fastapi import APIRouter
from model import  ErrorResponseModel
from database import fileInfoProcess, resultInfoProcess
from bson.objectid import ObjectId
# 初始化路由
router = APIRouter()
# # 初始化数据库驱动
fileinfoProcess = fileInfoProcess()
resultinfoProcess = resultInfoProcess()

@router.post("/detect", tags=["漏洞检测"])
async def detect(fileId:str):
    # 获取文件信息
    fileinfo = await fileinfoProcess.find({'_id': ObjectId(fileId)})
    if fileinfo:
        graph = fileinfo['graph']
        print(graph)
        # 检测
        re = fileinfo['graph'] #detector(graph)
        re_dict = {
            'fileId':ObjectId(fileId),
            'result':re,
        }
        reInfo = await resultinfoProcess.add(re_dict)

        return reInfo
    return ErrorResponseModel('error', '404', '找不到文件')
