from utils.model_util import model

full = None  # None | AIMessageChunk
for chunk in model.stream("物理和数学的区别是什么？用 100字以内回答"):
    full = chunk if full is None else full + chunk
    print(full.content)

print('='*50)