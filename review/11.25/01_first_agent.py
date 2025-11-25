from langchain_core.tools import tool

SYSTEM_PROMPT = """
你是一位擅长用双关语说话的天气预报专家。

你可以使用两个工具：
get_weather：用于获取特定地点的天气情况
get_user_location：用于获取用户的位置

如果用户向你询问天气，请务必确认地点。
"""

@tool
def get_weather(city: str):
    """获取特定地点的天气"""
    return f"{city}是晴天"

@tool
def get_user_location(user: str):
    """获取地点"""
    