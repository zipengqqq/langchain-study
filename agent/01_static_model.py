from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="deepseek-chat",
    api_key="api_key='sk-6cd9ca45e8d144d494628ee3feb40dca",
    base_url="https://api.deepseek.com/v1",
    max_tokens=1000,
    timeout=10
)