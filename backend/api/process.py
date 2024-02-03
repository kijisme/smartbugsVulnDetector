from fastapi import APIRouter
from model import ResponseModel, ErrorResponseModel
from database import fileInfoProcess, resultInfoProcess
from bson.objectid import ObjectId
from classifyModel import classifyModel

# 初始化路由
router = APIRouter()
# # 初始化数据库驱动
fileinfoProcess = fileInfoProcess()
resultinfoProcess = resultInfoProcess()
# 初始化模型
classify = classifyModel()

@router.post("/detect", tags=["漏洞检测"])
async def detect(fileId:str):
    # 获取文件信息
    fileinfo = await fileinfoProcess.find({'_id': ObjectId(fileId)})
    if fileinfo:
        graph = fileinfo['graph']
        # 检测
        re = classify.forward(graph)
        re_dict = {
            'fileId':ObjectId(fileId),
            'result':re,
        }
        reInfo = await resultinfoProcess.add(re_dict)

        return ResponseModel(reInfo, '200')
    return ErrorResponseModel('error', '404', '找不到文件')
