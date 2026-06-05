from llm import doubao_client

def generate_script_yaml(chunk_content: str) -> str:
    """
    将单段小说 → 标准 YAML 剧本
    """
    prompt = f"""
你是专业剧本编剧。
请将下面的小说内容，转换为标准的 YAML 剧本格式。
输出要求：
1. 只返回 YAML，不要任何多余解释
2. 固定字段：
   - scene: 场景序号
   - location: 地点
   - character: 角色
   - dialogue: 台词
   - action: 动作/描写

小说内容：
{chunk_content}
"""

    response = doubao_client.call(prompt, temperature=0.2)
    return response

def batch_generate_yaml(full_text: str):
    """
    全文小说 → 自动分片 → 批量生成剧本
    """
    from llm import split_text
    chunks = split_text(full_text)
    
    final_script = ""
    for i, chunk in enumerate(chunks, 1):
        print(f"正在生成第 {i} 段剧本...")
        yaml_script = generate_script_yaml(chunk)
        final_script += f"\n# ========== 第 {i} 段剧本 ==========\n"
        final_script += yaml_script
    
    return final_script