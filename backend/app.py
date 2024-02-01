from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/api/todo")
async def get_todo() -> int:
    return 1

@app.get("/api/todo{id}")
async def get_todo_by_id(id) -> int:
    return 1

@app.post("/api/todo")
async def post_todo() -> int:
    return 1

@app.put("/api/todo{id}")
async def put_todo(id, data) -> int:
    return 1

@app.delete("/api/todo/{id}")
async def delete_todo(id) -> int:
    return 1