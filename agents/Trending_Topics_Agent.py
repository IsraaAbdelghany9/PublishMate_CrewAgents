# agents/trending_agent.py
from Config.llm import basic_llm
from Config.shared import *
from Config.directories import *


class TrendingTopicsOutput(BaseModel):
    topics: List[Dict[str, str]] = Field(..., title="Trending topics with description", min_items=1)

def create_trending_topics_agent_task(user_input: str):
    agent = Agent(
        role="Trending Topics Identification Agent",
        goal="\n".join([
            f"You are an expert research assistant that identifies the latest trending topics in the field of {user_input}.",
            "Generate a detailed list of the top 3-5 trending topics or recent articles.",
            "Base your answer on recent publication trends, conferences, or journal articles.",
            "Output only a JSON object with a 'topics' list of objects with 'name' and 'description'."
        ]),
        backstory="Designed to guide users by providing the most relevant and current trending research topics.",
        llm=basic_llm,
        verbose=True,
    )

    task = Task(
        description="\n".join([
            f"Identify trending topics in the field of {user_input}.",
            "Provide 3 to 5 items with a brief description for each.",
            "Return JSON format with {name, description}."
        ]),
        expected_output="JSON object with trending topics and descriptions.",
        output_json=TrendingTopicsOutput,
        output_file=os.path.join(output_dir, "step_1_trending_topics.json"),
        agent=agent,
    )

    return agent, task
