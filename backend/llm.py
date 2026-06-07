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
        # 🔥 只改了这一行！换成你能用的 Doubao-Seed-1.6 模型ID
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
        请将以下小说内容转换为标准的YAML格式剧本。
        要求：
        1. 严格按照YAML语法输出
        2. 不要输出任何markdown代码块标记
        3. 结构包含novel_info和chapters两个部分
        4. chapters包含多个chapter，每个chapter包含多个scene，每个scene包含多个beat
        5. 每个beat包含action和dialogue两个字段

        小说内容：
        {novel_content}
        """
        
        result = self.generate_text(prompt)
        
        result = re.sub(r'^```yaml\s*', '', result)
        result = re.sub(r'^```\s*', '', result)
        result = re.sub(r'\s*```$', '', result)
        
        try:
            script = yaml.safe_load(result)
            return script
        except Exception as e:
            raise Exception(f"YAML解析失败: {str(e)}\n原始输出: {result}")