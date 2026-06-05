from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os,sys
# 固定拿到backend目录
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from script_generator import generate_script_yaml

router = APIRouter(prefix="/api/v1/script", tags=["剧本生成"])

class NovelReq(BaseModel):
    novel_content: str

@router.post("/generate")
def create_script(req: NovelReq):
    try:
        yaml_result = generate_script_yaml(req.novel_content)
        return {
            "code": 200,
            "msg": "success",
            "data": yaml_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败:{str(e)}")