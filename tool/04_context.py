from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

from utils.model_util import model

USER_DATABASE = {
    "user123": {
        "name": "Alice Johnson",
        "account_type": "Premium",
        "balance": 5000,
        "email": "alice@example.com"
    },
    "user456": {
        "name": "Bob Smith",
        "account_type": "Standard",
        "balance": 1200,
        "email": "bob@example.com"
    }
}

@dataclass
class UserContext:
    user_id: str

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """获取用户信息"""
    user_id = runtime.context.user_id

    if user_id in USER_DATABASE:
        user = USER_DATABASE[user_id]
        return f"用户信息是{user}"

    return f"该用户不存在"

agent = create_agent(
    model=model,
    tools=[get_account_info],
    context_schema=UserContext,
    system_prompt="你是一个经济专家"
)

result = agent.invoke(
    {'messages': [HumanMessage('我当前账号余额是多少')]},
    context=UserContext(user_id='user123')
)

print(result)