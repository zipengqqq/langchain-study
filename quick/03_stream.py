from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """
你是一位擅长用双关语说话的天气预报专家。
你可以使用两个工具：
get_weather_for_location：用于获取特定地点的天气情况
get_user_location：用于获取用户所在的位置
如果用户向你询问天气，请务必确认地点。如果你能从问题中判断出他们指的是自己当前所在的位置，请使用 get_user_location 工具来获取他们的位置。
"""


@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气情况。"""
    return f"在{city}，他总是晴天！"


@dataclass
class Context:
    user_id: str


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """获取当前用户的地理位置。"""
    user_id = runtime.context.user_id
    return "郑州" if user_id == "1" else "上海"


model = ChatOpenAI(
    model="deepseek-chat",
    api_key='sk-6cd9ca45e8d144d494628ee3feb40dca',
    base_url="https://api.deepseek.com/v1",  # 这个是必填的
    max_tokens=1000,
    timeout=10
)


@dataclass
class ResponseFormat:
    punny_response: str
    weather_condition: str | None = None


checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "外面天气怎么样，用五言绝句回复"}]},
#     config=config,
#     context=Context(user_id="1")
# )

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "外面天气怎么样，用五言绝句回复"}]
}, stream_mode="values"):
    # 每个块包含该时间点的完整状态
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(f"智能体：{latest_message.content}")
    elif latest_message.tool_calls:
        print(f"正在调用工具：{[tc['name'] for tc in latest_message.tool_calls]}")
# print(response['structured_response'])
