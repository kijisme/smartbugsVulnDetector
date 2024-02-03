import os
import subprocess
import networkx as nx
from fastapi import APIRouter, UploadFile, File
from bson.objectid import ObjectId

from model import ResponseModel, ErrorResponseModel
from database import fileInfoProcess, uploadInfoProcess

from graph.cfg import generate_cfg_graph
from graph.cg import generate_cg_graph
from graph.compress import generate_compress_graph
from graph.graph_utils import get_solc_version

# 初始化路由
router = APIRouter()
# 初始化数据库驱动
fileinfoProcess = fileInfoProcess()
uploadinfoProcess = uploadInfoProcess()

TMP_PATH = '/workspaces/smartbugsVulnDetector/tmp'

# 上传文件并处理后保存
@router.post("/upload", tags=["文件上传"])
async def upload(userId:str, file: UploadFile = File(...)):

    file_dict = await processFile(file)
    if file_dict:
        # 上传file数据库
        fileinfo = await fileinfoProcess.add(file_dict)
        upload_dict = {
            'fileId': ObjectId(fileinfo['_id']),
            'userId': ObjectId(userId),
            'status': 1,
        }
        # 上传upload数据库
        uploadinfo = await uploadinfoProcess.add(upload_dict)

        return ResponseModel(fileinfo,'200')
    return ErrorResponseModel("error.", 404, "编译错误")

async def processFile(file: UploadFile = File(...)):
    # 暂存文件
    content = await file.read()
    filename = file.filename
    content = content.decode('utf-8')
    file_path = os.path.join(TMP_PATH, 'tmp.sol')
    with open(file_path, "w") as f:
        f.write(content)
    version = get_solc_version(file_path)
    print(version)
    command = f"solc-select install {version}"
    subprocess.run(command, shell=True)

    if version is not None:
        try:
            # 生成图
            cfg = generate_cfg_graph(filename, file_path, version)
            cg = generate_cg_graph(filename, file_path, version)
            compress = generate_compress_graph(cfg, cg)
            nx.write_gpickle(cfg, os.path.join(TMP_PATH, 'cfg.gpickle'))
            nx.write_gpickle(cg, os.path.join(TMP_PATH, 'cg.gpickle'))
            nx.write_gpickle(compress, os.path.join(TMP_PATH, 'compress.gpickle'))
            
            # 保存
            fileinfo = {
                'filename' : file.filename,
                'content_type': file.content_type,
                'content' : content,
                'graph': compress,
            }
            return fileinfo
        except Exception as e:
           print(e)
    


