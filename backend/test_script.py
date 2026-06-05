from script_generator import batch_generate_yaml

test_text = """
雨夜的小巷里，小明靠在墙上，手里拿着一封信。
小红撑着伞走过来。
小红：你找我？
小明：这封信，你必须看。
"""

if __name__ == "__main__":
    result = batch_generate_yaml(test_text)
    print("\n===== 生成完成 =====\n")
    print(result)