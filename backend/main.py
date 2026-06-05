from fastapi import FastAPI
from api.script_api import router

app = FastAPI(title="剧本生成接口")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)