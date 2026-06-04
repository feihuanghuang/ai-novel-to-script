from llm import doubao_client, split_text

# 测试文本分块
test_text = """
第一章 初遇

张三走在大街上，突然看到一个熟悉的身影。

"李四！"他喊道。

李四转过头，惊讶地看着他："张三？你怎么在这里？"

"我来这里出差，"张三说，"没想到会遇到你。"

两人找了一家咖啡馆，坐下来聊了起来。
"""

print("=== 测试文本分块 ===")
chunks = split_text(test_text)
print(f"分块数量: {len(chunks)}")
print(f"第一块内容:\n{chunks[0]}\n")

print("=== 测试大模型调用 ===")
try:
    response = doubao_client.call("你好，请用一句话介绍一下自己")
    print(f"大模型响应: {response}")
    print("\n✅ 大模型调用成功！")
except Exception as e:
    print(f"❌ 大模型调用失败: {e}")