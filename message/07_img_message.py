import base64
from utils.model_util import model

# 从本地文件读取图片并转为 Base64
with open("data/img.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

message = {
    'role': 'user',
    'content': [
        {'type': 'text', 'text': '这些图片有哪些文字'},
        {
            'type': 'image_url',  # ✅ 使用 image_url
            'image_url': {
                'url': f'data:image/png;base64,{encoded_string}'
            }
        }
    ]
}

response = model.invoke([message])
print(response)