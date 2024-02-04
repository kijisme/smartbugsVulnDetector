import os
import subprocess
import networkx as nx
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from bson.objectid import ObjectId
from datetime import datetime

from model import  ResponseModel
from database import fileInfoProcess, uploadInfoProcess

from graph.cfg import generate_cfg_graph
from graph.cg import generate_cg_graph
from graph.compress import generate_compress_graph
from graph.graph_utils import get_solc_version

from dep import get_current_user

# 初始化路由
router = APIRouter()
# 初始化数据库驱动
fileinfoProcess = fileInfoProcess()
uploadinfoProcess = uploadInfoProcess()

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

    return ResponseModel(fileinfo, True,'处理完成')

async def processFile(file: UploadFile = File(...)) -> dict:
    # 暂存文件
    content = await file.read()
    filename = file.filename
    content = content.decode('utf-8')
    file_path = os.path.join(TMP_PATH, 'tmp.sol')
    with open(file_path, "w") as f:
        f.write(content)
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
    

        
@router.post("/history", tags=["登录接口"])
async def history(userinfo: dict = Depends(get_current_user)) -> dict:
    userId = userinfo['_id']
    response = await uploadinfoProcess.find_all({'userId':ObjectId(userId)})