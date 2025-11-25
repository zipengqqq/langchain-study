from langchain.messages import RemoveMessage
from langchain.tools import tool
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.types import Command


@tool
def clear_conversation() -> Command:
    """清空历史对话"""
    return Command(
        update={
            'messages': [RemoveMessage(id=REMOVE_ALL_MESSAGES)]
        }
    )

@tool
def update_user_name(new_name: str) -> Command:
    """更新用户姓名"""
    return Command(update={'user_name': new_name})