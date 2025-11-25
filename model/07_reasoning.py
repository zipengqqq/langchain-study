from utils.model_util import model

"""通义千问不支持推理步骤显示"""
for chunk in model.stream("数学和物理哪个更难？"):
    print(chunk)