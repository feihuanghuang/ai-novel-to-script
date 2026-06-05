import os
import yaml
import requests
from dotenv import load_dotenv

load_dotenv()


class DoubaoClient:
    # 单例模式实现
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.api_key = os.getenv("DOUBAO_API_KEY")
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        self.model = "doubao-seed-1-6-251015"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate_text(self, prompt: str, temperature: float = 0.3) -> str:
        """统一的大模型调用方法"""
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": 4096
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"豆包API调用失败: {str(e)}")

    def split_text(self, text: str, chunk_size: int = 3000, chunk_overlap: int = 300) -> list[str]:
        """小说内容智能分片方法"""
        if not text:
            return []

        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current_chunk) + len(para) > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    # 剧本YAML生成专用方法
    def generate_script_yaml(self, novel_content: str) -> dict:
        """
        将小说内容转换为标准YAML格式的剧本
        返回解析后的字典，调用失败抛出异常
        """
        prompt = f"""
请将以下小说片段转换为标准YAML格式的剧本，严格遵循以下规则：
1. 只输出YAML内容，不要任何解释、说明、开场白或结束语
2. 不要在YAML前后添加```yaml或```标记
3. 必须包含以下字段：
   - title: 剧本标题（从内容提取）
   - scene: 场景描述（时间、地点、环境）
   - characters: 出场人物列表（数组）
   - dialogues: 对话列表，每个对话包含：
     - speaker: 说话人
     - content: 台词内容
     - action: 动作/神态描述（可选）
4. 保持语义完整，不要删减关键情节
5. YAML语法必须严格正确，缩进使用2个空格

小说内容：
{novel_content}
"""

        # 调用大模型
        raw_response = self.generate_text(prompt)

        # 清理可能的markdown标记
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```yaml"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()

        # 解析YAML并返回
        try:
            return yaml.safe_load(cleaned_response)
        except yaml.YAMLError as e:
            raise Exception(f"YAML解析失败: {str(e)}\n原始输出: {cleaned_response}")


# 全局单例实例
doubao_client = DoubaoClient()