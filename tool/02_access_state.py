from langchain.tools import tool, ToolRuntime


@tool
def summary_conversation(runtime: ToolRuntime) -> str:
    messages = runtime.state['messages']

    human_msgs = sum([1 for m in messages if m.__class__.__name__ == "HumanMessage"])
    ai_msgs = sum([1 for m in messages if m.__class__.__name__ == "AIMessage"])
    tool_msgs = sum([1 for m in messages if m.__class__.__name__ == "ToolMessage"])

    return f"人类消息有{human_msgs}条；AI 消息有{ai_msgs}条；工具消息有{tool_msgs}条"

@tool
def get_user_preference(
        pref_name: str,
        runtime: ToolRuntime
) -> str:
    """"获取用户偏好设置的值"""
    preferences = runtime.state.get('user_preferences', {})
    return preferences.get(pref_name, "还未设置")