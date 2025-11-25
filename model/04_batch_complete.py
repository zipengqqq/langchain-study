from utils.model_util import model

input = [f'1+{item}等于多少？' for item in range(10)]

res_list = model.batch_as_completed(input)
# res_list = model.batch_as_completed(
#     input,
#     config={'max_concurrency': 5} # 控制并发数量
# )


"""这种方式会将结果一个一个使用流式输出"""
for res in res_list:
    print(res)
