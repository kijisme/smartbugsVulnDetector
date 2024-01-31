from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class PresetInfo(BaseModel):
    presetInfo: str

@app.post("/send-info" ,tags=["send-info"])
async def send_info(preset_info: PresetInfo):
    print("Received preset info:", preset_info.presetInfo)
    # 在这里可以添加处理预设信息的逻辑
    return {
        "status": "success", "message": "Info received successfully"
        }

# curl -X POST http://localhost:8000/send-info -d '{"presetInfo":"111"}' -H 'Content-Type: application/json'