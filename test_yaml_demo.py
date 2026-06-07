import yaml
from backend.llm import doubao_client

# 测试用例1：正常短文本（最基础场景）
print("=== 测试1：正常短文本 ===")
test_content1 = """
小明推开门，看到小红正站在窗边望着外面的雨。
小明："你怎么来了？外面雨这么大。"
小红转过身，手里拿着一本厚厚的书，笑着说："我来给你送上次你借我的那本《百年孤独》。"
小明："太感谢了！快进来坐，我给你倒杯热水。"
"""

try:
    script1 = doubao_client.generate_script_yaml(test_content1)
    print("✅ 生成成功！")
    print(yaml.dump(script1, allow_unicode=True, indent=2))
except Exception as e:
    print(f"❌ 生成失败：{e}")

# 测试用例2：空文本（边界条件）
print("\n=== 测试2：空文本 ===")
try:
    script2 = doubao_client.generate_script_yaml("")
    print("❌ 应该失败但成功了")
except Exception as e:
    print(f"✅ 正确抛出异常：{e}")

# 测试用例3：纯空格文本（边界条件）
print("\n=== 测试3：纯空格文本 ===")
try:
    script3 = doubao_client.generate_script_yaml("   \n\n   ")
    print("❌ 应该失败但成功了")
except Exception as e:
    print(f"✅ 正确抛出异常：{e}")