from langchain.agents.chat.prompt import HUMAN_MESSAGE
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from utils.model_util import model

# invoke 调用
print('='*50)
response1 = model.invoke('中国时间，今天星期几？')
print(response1)


# 多轮对话
print('='*50)
conversation = [
    {"role": "system", "content": "你是一个乐于助人的助手，专门将英文翻译成中文。"},   # 系统提示
    {"role": "user", "content": "翻译：I love you."}, # 用户身份
    {"role": "assistant", "content": "我爱你"},    # LLM 身份，即 LLM 做出的响应
    {"role": "user", "content": "翻译：I like apple."}
]
response2 = model.invoke(conversation)
print(response2)

# 消息对象
print('='*50)
conversation = [
    SystemMessage('你是一个乐于助人的助手，专门将英文翻译成中文。'),
    HumanMessage('I love you.'),
    AIMessage('我爱你'),
    HumanMessage('I like apple and dog.')
]
response3 = model.invoke(conversation)
print(response3)