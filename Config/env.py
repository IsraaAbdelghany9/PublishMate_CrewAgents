# Config/env.py
from Config.shared import *

load_dotenv()

# Get all env vars
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PROJECT_ID = os.getenv("PROJECT_ID")
# PROJECT_NAME = os.getenv("PROJECT_NAME")

# Configure Google GenAI
# genai.configure(api_key=OPENAI_API_KEY)

# Init AgentOps
agentops.init(
    api_key=AGENTOPS_API_KEY,
    skip_auto_end_session=True,
    default_tags=["crewai"]
)
