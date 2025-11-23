from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel

from utils.model_util import model


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model=model,
    response_format=ToolStrategy(ContactInfo)
)

res = agent.invoke({
    "messages": [{"role": "user", "content": "提取联系人信息：訾鹏，2857820263@qq.com，19545640177"}]
})

print(res['structured_response'])

# res['structured_response'] 是一个对象，可以访问其中的元素
print(res['structured_response'].name)
