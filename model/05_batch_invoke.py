from utils.model_util import model

input = [f'1+{item}等于多少？' for item in range(10)]


res_list = model.batch(input)
# res_list = model.batch(
#     input,
#     config={'max_concurrency': 5} # 控制并发数量
# )

for res in res_list:
    print('\n\n')
    print(res)