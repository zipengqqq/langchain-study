from langchain_core.messages import SystemMessage, HumanMessage

from utils.model_util import model

messages = [
    SystemMessage('使用五言绝句回答'),
    HumanMessage('我今天好饿')
]

response = model.invoke(messages)

print(response)