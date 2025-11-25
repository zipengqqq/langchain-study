from langchain.tools import tool, ToolRuntime

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """获取天气"""
    writer = runtime.stream_writer

    writer(f"正在查询城市相关数据：{city}")
    writer(f"城市的相关数据是：{city}")

    return "它是晴天"