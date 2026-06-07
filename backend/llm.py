from openai import OpenAI
import yaml
import re

class DoubaoClient:
    def __init__(self, api_key, base_url="https://ark.cn-beijing.volces.com/api/v3"):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=500
        )
        self.model = "doubao-seed-1-6-251015"
        self.temperature = 0.3

    def generate_text(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            response_format={"type": "text"}
        )
        return response.choices[0].message.content

    def generate_script_yaml(self, novel_content):
        prompt = f"""
你是专业短剧编剧，将小说转为【标准分镜头剧本YAML】。
严格遵守以下规则：
1. 只输出纯YAML，不要任何解释
2. 不要输出 ``` 代码块
3. 结构必须如下：

title: 短剧标题
summary: 剧情简介（30字）
scenes:
  - scene_id: S01
    location: 场景地点
    time: 日/夜
    shots:
      - shot_id: 1
        frame: 远景/全景/中景/近景/特写
        duration: 秒（数字）
        visual: 画面描述
        audio: 角色名(情绪):台词 或 【音效】

小说内容：
{novel_content}
"""
        result = self.generate_text(prompt)
        result = re.sub(r'^```yaml', '', result, flags=re.MULTILINE)
        result = re.sub(r'^```', '', result, flags=re.MULTILINE)
        result = re.sub(r'```$', '', result, flags=re.MULTILINE)

        try:
            script = yaml.safe_load(result)
            return script
        except Exception as e:
            raise Exception(f"YAML解析失败: {str(e)}\n输出:{result}")