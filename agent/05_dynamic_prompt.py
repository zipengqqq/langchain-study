from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest


class Context(TypedDict):
    """
        TypeDict 是一种类型提示工具，用于对字典的键和对应值的类型进行类型检查
    """
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """基于角色生成系统提示词"""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "你是一个乐于助人的助手。"

    if user_role == "expert":
        return f"{base_prompt} 请使用技术用语回答。"
    elif user_role == "beginner":
        return f"{base_prompt} 请使用生动易懂的语言来解释。"

    return base_prompt

agent = create_agent(
    model="gpt-4o",
    middleware=[user_role_prompt],
    context_schema=Context
)

res = agent.invoke(
    {"messages": [{"role": "user", "content": "什么是机器学习？"}]},
     context={"user_role": "expert"}
)