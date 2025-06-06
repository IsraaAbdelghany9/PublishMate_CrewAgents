import os
from typing import List, Dict
from pydantic import BaseModel, Field

class TrendingTopicsOutput(BaseModel):
    topics: List[Dict[str, str]] = Field(..., title="Trending topics with description", min_items=1)

trending_topics_agent = Agent(
    role="Trending Topics Identification Agent",

    goal="\n".join([
        f"You are an expert research assistant that identifies the latest trending topics in the field of {user_input} only focus on it .",
        "Generate a detailed list of the top 3-5 trending topics or recent articles reflecting advances and high interest in this field.",
        "Base your answer on recent publication trends, conferences, or journal articles.",
        "Do not include unrelated or general topics.",
        "Output only a JSON object with a 'topics' list containing objects with 'name' and 'description'."
    ]),
    backstory="Designed to guide users by providing the most relevant and current trending research topics in their specified field.",
    llm=basic_llm,
    verbose=True,
)

trending_topics_task = Task(
    description="\n".join([
        f"you are an expert in a {user_input} field to help beginner researchers in their writings .",
        "Provide a list of 3 to 5 trending topics or articals with a brief description for each.",
        "Focus on recent research interests supported by publication trends.",
        "Output in JSON format with 'topics' as list of objects {name, description}."
    ]),
    expected_output="JSON object with list of trending topics and descriptions.",
    output_json=TrendingTopicsOutput,
    output_file=os.path.join(output_dir, "step_1_trending_topics.json"),
    agent=trending_topics_agent,
)