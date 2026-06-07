from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, Script
import yaml
import os

app = FastAPI(title="AI小说转剧本工具")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路径重定向到首页
@app.get("/")
async def root():
    return RedirectResponse(url="/index.html")

# 请求模型
class NovelRequest(BaseModel):
    content: str
    script_type: str = "short_drama"
    model: str = "doubao"
    api_key: str  # 接收前端传来的API密钥

class SaveScriptRequest(BaseModel):
    title: str
    script_type: str
    novel_content: str
    yaml_content: str

# 剧本生成接口 —— 多模型适配版
@app.post("/api/generate-script")
async def generate_script(request: NovelRequest):
    try:
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="小说内容不能为空")
        
        if not request.api_key.strip():
            raise HTTPException(status_code=400, detail="请输入API密钥")

        script = None
        model_name = request.model

        # 豆包系列
        if model_name.startswith("doubao-"):
            from backend.llm import DoubaoClient
            client = DoubaoClient(api_key=request.api_key)
            client.model = model_name
            script = client.generate_script_yaml(request.content)

        # DeepSeek系列
        elif model_name.startswith("deepseek-"):
            from backend.llm import DeepSeekClient
            client = DeepSeekClient(api_key=request.api_key, model=model_name)
            script = client.generate_script_yaml(request.content)

        # 通义千问系列
        elif model_name.startswith("qwen"):
            from backend.llm import QwenClient
            client = QwenClient(api_key=request.api_key, model=model_name)
            script = client.generate_script_yaml(request.content)

        else:
            raise HTTPException(status_code=400, detail=f"不支持的模型：{model_name}")

        return {
            "success": True,
            "script": script,
            "yaml": yaml.dump(script, allow_unicode=True, indent=2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 保存剧本接口
@app.post("/api/scripts")
async def save_script(script_request: SaveScriptRequest, db: Session = Depends(get_db)):
    try:
        db_script = Script(
            title=script_request.title,
            script_type=script_request.script_type,
            novel_content=script_request.novel_content,
            yaml_content=script_request.yaml_content
        )
        db.add(db_script)
        db.commit()
        db.refresh(db_script)
        
        return {
            "success": True,
            "id": db_script.id,
            "message": "剧本保存成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取所有剧本接口
@app.get("/api/scripts")
async def get_all_scripts(db: Session = Depends(get_db)):
    scripts = db.query(Script).order_by(Script.created_at.desc()).all()
    return [
        {
            "id": script.id,
            "title": script.title,
            "script_type": script.script_type,
            "created_at": script.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for script in scripts
    ]

# 获取单个剧本接口
@app.get("/api/scripts/{script_id}")
async def get_script(script_id: int, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="剧本不存在")
    
    return {
        "id": script.id,
        "title": script.title,
        "script_type": script.script_type,
        "novel_content": script.novel_content,
        "yaml_content": script.yaml_content,
        "created_at": script.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

# 删除剧本接口
@app.delete("/api/scripts/{script_id}")
async def delete_script(script_id: int, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="剧本不存在")
    
    db.delete(script)
    db.commit()
    
    return {
        "success": True,
        "message": "剧本删除成功"
    }

# 健康检查接口
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "0.5.0"}

# 静态文件挂载
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    import logging
    import sys

    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s:     %(message)s",
        stream=sys.stdout
    )

    print("\n" + "="*50)
    print("✅ AI小说转剧本工具启动成功！")
    print("📱 本地访问：http://localhost:8000")
    print("💻 局域网访问：http://你的电脑IP:8000")
    print("⏹️  按 Ctrl+C 停止服务")
    print("="*50 + "\n")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        timeout_keep_alive=500,
        log_level="warning"
    )