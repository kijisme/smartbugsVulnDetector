import os

from fastapi import APIRouter, UploadFile, File
from bson.objectid import ObjectId
from database import fileInfoProcess, uploadInfoProcess

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

        return fileinfo

async def processFile(file: UploadFile = File(...)):
    # 暂存文件
    content = await file.read()
    content = content.decode('utf-8')
    file_path = os.path.join(TMP_PATH, 'tmp.sol')
    with open(file_path, "w") as f:
        f.write(content)
    try:
        # 生成图
        cfg = 'cfg'#generate_cfg_graph(file_path)
        cg = 'cg'#generate_cg_graph(file_path)
        compress = cfg + cg #generate_compress_graph(file_path)
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


