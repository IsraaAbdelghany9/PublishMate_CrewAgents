from Config.shared import TavilyClient
from Config.env import TAVILY_API_KEY
from Config.shared import *
import json
import os

@tool
def search_engine_tool(query: str):
    """Search for relevant results using the Tavily search client."""
    search_client = TavilyClient(api_key=TAVILY_API_KEY)
    results = search_client.search(query)

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Save to output/tool_output.json
    with open("output/tool_output.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n\nSearch results saved in 'output/tool_output.json'\n\n")
    return results
