from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain_openai import ChatOpenAI

basic_model = ChatOpenAI(model="gpt-4o-mini") # 基础模型
advanced_model = ChatOpenAI(model="gpt-4o") # 高级模型

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """根据对话复杂性，使用模型"""
    message_count = len(request.state['messages'])

    model = basic_model if message_count > 100 else advanced_model

    return handler(request.override(model=model))

agent = create_agent(
    model=basic_model, # 默认使用基础模型
    middleware=[dynamic_model_selection]
)