from langchain_openai import ChatOpenAI

# 使用通义千问（Qwen-Max 示例）
model = ChatOpenAI(
    model="qwen-max",  # 可选: qwen-turbo, qwen-plus, qwen-max, qwen-long 等
    api_key="sk-c731b0bcdec6419fb338717e2717ae63",  # 替换为你自己的 key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    max_tokens=10000,
    timeout=60,
    max_retries=3 # 最大重试次数
)

# 测试调用
response = model.invoke("李白有哪些著名诗作？")
print(response.content)