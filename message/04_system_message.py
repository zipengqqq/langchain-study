from langchain_core.messages import SystemMessage, HumanMessage

from utils.model_util import model

system = SystemMessage('你是一位资深的 Python 开发人员，精通各类 Web 框架，请提供代码示例并解释思路，解释要简明扼要')

messages = [
    system,
    HumanMessage('fastapi是什么，如何快速入门')
]

res = model.invoke(messages)

print(res)