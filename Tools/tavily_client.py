from Config.shared import TavilyClient
from Config.env import TAVILY_API_KEY
from Config.shared import *
 
@tool
def search_engine_tool(query: str):
    """Useful for search-based queries. Use this to find current information about any query related pages using a search engine"""
    search_client = TavilyClient(api_key=TAVILY_API_KEY)
    return search_client.search(query)
