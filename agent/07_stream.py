from langchain.agents import create_agent

from utils.model_util import model

agent = create_agent(
    model=model
)

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "李白有哪些作品"}]
}, stream_mode="values"):
    latest_message = chunk["messages"][-1]
    print(f"智能体：{latest_message.content}")

