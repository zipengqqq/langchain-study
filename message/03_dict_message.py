from utils.model_util import model

messages = [
    {'role': 'system', 'content': '你是一个诗人'},
    {'role': 'user', 'content': '先一个关于春天的故事'},
]

res = model.invoke(messages)

print(type(res))
print(res)