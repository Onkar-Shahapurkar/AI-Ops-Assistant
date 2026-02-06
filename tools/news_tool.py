import os
import requests
from dotenv import load_dotenv
from core.utils import safe_api_call
from tools.base_tool import BaseTool
from core.tool_registry import ToolRegistry

load_dotenv()

class NewsTool(BaseTool):

    def name(self) -> str:
        return "news_tool"

    def run(self, query: str):
        api_key = os.getenv("NEWS_API_KEY")
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"

        data = safe_api_call(requests.get, url).json()

        articles = []
        for a in data.get("articles", [])[:5]:
            articles.append({
                "title": a["title"],
                "source": a["source"]["name"],
                "published_at": a["publishedAt"]
            })

        return {"query": query, "articles": articles}

ToolRegistry.register("news_tool", NewsTool)
