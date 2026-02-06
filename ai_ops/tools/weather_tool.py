import requests
from core.utils import safe_api_call
from tools.base_tool import BaseTool
from core.tool_registry import ToolRegistry

class WeatherTool(BaseTool):

    def name(self) -> str:
        return "weather_tool"

    def run(self, city: str):
        city_map = {
            "mumbai": (19.0760, 72.8777),
            "delhi": (28.6139, 77.2090),
            "pune": (18.5204, 73.8567),
            "bangalore": (12.9716, 77.5946)
        }

        lat, lon = city_map.get(city.lower(), (19.0760, 72.8777))

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

        data = safe_api_call(requests.get, url).json()

        return {
            "city": city,
            "temperature": data["current_weather"]["temperature"],
            "windspeed": data["current_weather"]["windspeed"]
        }

ToolRegistry.register("weather_tool", WeatherTool)
