from typing import Any

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.store.memory import InMemoryStore

from utils.model_util import model


@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """查看用户信息"""
    store = runtime.store
    user_info = store.get(("users", ), user_id)

    return str(user_info.value) if user_info else "未知用户"

@tool
def save_user_info(user_id: str, user_info: dict[str, Any], runtime: ToolRuntime) -> str:
    """保存用户信息"""
    store = runtime.store
    store.put(("users",), user_id, user_info)
    return f"成功保存用户信息"

store = InMemoryStore()
agent = create_agent(
    model=model,
    tools=[get_user_info, save_user_info],
    store=store
)

# 保存信息
agent.invoke({
    'messages': [{'role': 'user', 'content': '保存以下信息: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev'}]
})

# 获取信息
res = agent.invoke({
    'messages': [{'role': 'user', 'content': '获取id是abc123用户的信息'}]
})

print(res)



