from pydantic import BaseModel, Field

from utils.model_util import model


class Movie(BaseModel):
    title: str = Field(..., description="电影名字")
    year: int = Field(..., description="电影发布年份")
    director: str = Field(..., description="电影作者")

model = model.with_structured_output(Movie)

query = """
请提取电影信息并以json格式返回。字段名为title、year、director

《阿甘正传》（Forrest Gump）是一部经典的美国励志剧情片。

导演是罗伯特·泽米吉斯（Robert Zemeckis）。
影片于1994年上映，具体在美国的公映日期是1994年7月6日。

主演包括汤姆·汉克斯（饰演阿甘）、罗宾·怀特（饰演珍妮）、加里·辛尼斯（饰演丹中尉）、麦凯尔泰·威廉逊（饰演布巴）以及莎莉·菲尔德（饰演阿甘的母亲）。

电影改编自温斯顿·格鲁姆于1986年出版的同名小说。故事讲述了一位智商不高但心地善良的男子阿甘，如何在20世纪后半叶的美国历史中意外参与众多重大事件，并以纯真的态度影响了周围的人和世界。

影片类型为剧情与爱情，片长约142分钟，语言为英语，制片国家为美国。

《阿甘正传》在第67届奥斯卡金像奖上获得了包括最佳影片、最佳导演和最佳男主角在内的六项大奖，成为影史经典之一。全球票房超过10亿美元，广受观众和评论界好评。

"""

response = model.invoke(query)

print(response) # title='阿甘正传' year=1994 director='罗伯特·泽米吉斯'