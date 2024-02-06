from fastapi import APIRouter, Depends, Body, HTTPException
from model import detectInfo, ResponseModel
from api.common import fileinfoProcess, resultinfoProcess, uploadinfoProcess
from bson.objectid import ObjectId
from classifyModel import classifyModel
from dep import get_current_user
import networkx as nx
from datetime import datetime

# 初始化路由
router = APIRouter()
# 初始化模型
classify = classifyModel()

@router.post("/detect", tags=["漏洞检测"])
async def detect(userinfo: dict = Depends(get_current_user), detectinfo:detectInfo = Body(...)) ->ResponseModel :
    useId = userinfo['_id']
    fileId = detectinfo.fileId
    # 获取文件信息
    fileinfo = await fileinfoProcess.find({'_id': ObjectId(fileId)})

    if fileinfo is not None:
        # 更改时间字段
        detector_time = datetime.utcnow()
        updateinfo = await uploadinfoProcess.update({'fileId': ObjectId(fileId),'userId':ObjectId(useId)}, 
                                                        {'detector_time': detector_time})
        if updateinfo is not None:
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

            return ResponseModel(reInfo, True, '/process/detect')
        raise HTTPException(status_code=500, detail="数据库操作失败")
    raise HTTPException(status_code=500, detail="invalid file")

# 获取文件report
@router.post("/report", tags=["文件主页"])
async def report(userinfo: dict = Depends(get_current_user), detectinfo:detectInfo = Body(...)) -> ResponseModel :
    userId = userinfo['_id']
    fileId = detectinfo.fileId
    
    # 查询文件信息上传信息
    uploadinfo = await uploadinfoProcess.find({'fileId': ObjectId(fileId), 'userId': ObjectId(userId)})
    if uploadinfo is not None:
        # 获取文件信息
        fileinfo = await fileinfoProcess.find({'_id': ObjectId(fileId)})
        if fileinfo is not None:
            # 文件未检测
            if uploadinfo['detector_time'] is not None:
                # 获取文件检测信息
                resultinfo = await resultinfoProcess.find({'fileId': ObjectId(fileId)})
                if resultinfo is not None:
                    return ResponseModel({'fileinfo' : fileinfo, 'resultInfo': resultinfo}, True, '返回历史检测结果')
            return ResponseModel({'fileinfo' : fileinfo}, True, '/process/report')
        else:
            raise HTTPException(status_code=404, detail="file not found")
    raise HTTPException(status_code=404, detail="upload not found")

