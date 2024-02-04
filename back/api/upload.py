import os
import subprocess
import networkx as nx
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta

from model import  ResponseModel
from api.common import fileinfoProcess, uploadinfoProcess

from graph.cfg import generate_cfg_graph
from graph.cg import generate_cg_graph
from graph.compress import generate_compress_graph
from graph.graph_utils import get_solc_version

from dep import get_current_user

# 初始化路由
router = APIRouter()

TMP_PATH = '/workspaces/smartbugsVulnDetector/tmp'

# 上传文件并处理后保存
@router.post("/upload", tags=["文件上传"])
async def upload(userinfo: dict = Depends(get_current_user), file: UploadFile = File(...)) -> ResponseModel:
    userId = userinfo['_id']
    file_dict = await processFile(file)
    # 上传file数据库
    fileinfo = await fileinfoProcess.add(file_dict)
    upload_dict = {
        'fileId': ObjectId(fileinfo['_id']),
        'userId': ObjectId(userId),
        'upload_time': datetime.utcnow(),
        'detector_time': None,
    }
    # 上传upload数据库
    await uploadinfoProcess.add(upload_dict)

    return ResponseModel(fileinfo, True,'/upload/upload')

async def processFile(file: UploadFile = File(...)) -> dict:
    # 暂存文件
    content = await file.read()
    filename = file.filename
    content = content.decode('utf-8')
    file_path = os.path.join(TMP_PATH, 'tmp.sol')
    with open(file_path, "w") as f:
        f.write(content)
    # 设置版本
    version = get_solc_version(file_path)
    command = f"solc-select install {version}"
    subprocess.run(command, shell=True)

    if version is not None:
        try:
            # 生成图
            cfg = generate_cfg_graph(filename, file_path, version)
            cg = generate_cg_graph(filename, file_path, version)
            compress = generate_compress_graph(cfg, cg)
            # nx.write_gpickle(cfg, os.path.join(TMP_PATH, 'cfg.gpickle'))
            # nx.write_gpickle(cg, os.path.join(TMP_PATH, 'cg.gpickle'))
            # nx.write_gpickle(compress, os.path.join(TMP_PATH, 'compress.gpickle'))
            
            compress_dict = nx.readwrite.json_graph.node_link_data(compress)

            fileinfo = {
                'filename' : file.filename,
                'content_type': file.content_type,
                'content' : content,
                'graph':  compress_dict,
            }
            return fileinfo
        except Exception as e:
           raise HTTPException(status_code=500, detail="编译错误")
    else:
        raise HTTPException(status_code=500, detail="编译器错误")
    

        
@router.post("/history", tags=["历史上传记录"])
async def history(userinfo: dict = Depends(get_current_user)) -> ResponseModel:
    userId = userinfo['_id']

    today = datetime.utcnow()
    start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = start_of_day - timedelta(days=1)
    previous7 = start_of_day - timedelta(days=7)

    # 大于等于 小于
    condition_today = {"$gte": start_of_day, "$lt": today}
    condition_yesterday = {"$gte": yesterday, "$lt": today}
    condition_previous7 = {"$gte": previous7, "$lt": yesterday}

    response_today = await uploadinfoProcess.find_all({'userId':ObjectId(userId), 'upload_time':condition_today})
    response_yesterday = await uploadinfoProcess.find_all({'userId':ObjectId(userId), 'upload_time':condition_yesterday})
    response_previous7 = await uploadinfoProcess.find_all({'userId':ObjectId(userId), 'upload_time':condition_previous7})

    return ResponseModel({'today':response_today, 'yesterday':response_yesterday, 'previous':response_previous7}, True, 'upload/history')