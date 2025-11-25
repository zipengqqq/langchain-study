from typing import Literal

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class WeatherInput(BaseModel):
    """用于天气查询输入"""
    location: str = Field(description='城市名称或坐标')
    units: Literal['celsius', 'fahrenheit'] = Field(default='celsius', description="温度单位偏好")
    include_forecast: bool = Field(default=False, description="是否包含未来5天的天气预报")

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """获取天气"""
    temp = 22 if units == 'celsius' else 72

    result = f"{location}当前天气：{temp}度{units[0].upper()}"

    if include_forecast:
        result += "\b未来 5 天天气预报：晴朗"
    return result