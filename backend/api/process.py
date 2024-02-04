from fastapi import APIRouter, Depends, Body, HTTPException
from model import detectInfo, ResponseModel
from database import fileInfoProcess, resultInfoProcess, uploadInfoProcess
from bson.objectid import ObjectId
from classifyModel import classifyModel
from dep import get_current_user
import networkx as nx
from datetime import datetime

# 初始化路由
router = APIRouter()
# # 初始化数据库驱动
fileinfoProcess = fileInfoProcess()
resultinfoProcess = resultInfoProcess()
uploadinfoProcess = uploadInfoProcess()
# 初始化模型
classify = classifyModel()

@router.post("/detect", tags=["漏洞检测"])
async def detect(userinfo: dict = Depends(get_current_user), detectinfo:detectInfo = Body(...)) ->ResponseModel :
    fileId = detectinfo.fileId
    # 获取文件信息
    fileinfo = await fileinfoProcess.find({'_id': ObjectId(fileId)})
    # 获取上传记录
    uploadinfo = await uploadinfoProcess.find({'fileId':ObjectId(fileId)})
    # 检测是否检测过
    if uploadinfo['detector_time'] is None:
        # 更改时间字段
        detector_time = datetime.utcnow()
        await uploadinfoProcess.update({'fileId': ObjectId(fileId)}, {'detector_time': detector_time})
        # 检测
        graph_dict = fileinfo['graph']
        # 数据预处理
        graph = nx.node_link_graph(graph_dict)
        # 检测
        re = classify.forward(graph)
        # 添加到数据库
        re_dict = {
            'fileId':ObjectId(fileId),
            'result':re,
        }
        reInfo = await resultinfoProcess.add(re_dict)

    else:
        # 查看re历史
        reInfo = await resultinfoProcess.find({"fileId":ObjectId(fileId)})
    
    return ResponseModel(reInfo, True, '返回历史检测结果')
