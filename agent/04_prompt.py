from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt")
agent = create_agent(
    model,
    system_prompt="你是一个乐于助人的助手，请简洁并准备回答问题。"
)