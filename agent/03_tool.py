from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.messages import ToolMessage

@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"404"

@tool
def get_weather(location: str) -> str:
    """获取某个地方的天气"""
    return f"{location}是晴天"

@wrap_tool_call
def handle_tool_errors(request, handler):
    """使用自定义消息来处理工具执行过程中发生的错误"""
    # 如果有错误发生，那么会返回一个响应，该响应返回给LLM，LLM会对此调整
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"工具调用失败：请检查你的输入并且再次重试。错误为：{str(e)}",
            tool_call_id=request.tool_call["id"]
        )

model = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(model, tools=[search, get_weather])