from fastapi import APIRouter, Depends, Body
from model import  ErrorResponseModel, detectInfo
from database import fileInfoProcess, resultInfoProcess
from bson.objectid import ObjectId
# 初始化路由
router = APIRouter()
# # 初始化数据库驱动
fileinfoProcess = fileInfoProcess()
resultinfoProcess = resultInfoProcess()

@router.post("/detect", tags=["漏洞检测"])
async def detect(info: detectInfo = Depends()):
    # 获取文件信息
    fileinfo = await fileinfoProcess.find({'content_type':info.contentType})
    if fileinfo:
        graph = fileinfo['graph']
        # 检测
        re = fileinfo['graph'] #detector(graph)
        re_dict = {
            'fileId':info.fileId,
            'result':re,
        }
        reInfo = await resultinfoProcess.add(re_dict)

        return reInfo
    return ErrorResponseModel('error', '404', '找不到文件')
