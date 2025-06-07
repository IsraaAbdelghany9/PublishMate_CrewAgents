# main.py

from agents.Trending_Topics_Agent import create_trending_topics_agent_task
from agents.Recent_Papers_Retrieval_Agent import create_recent_papers_agent_task
from agents.Research_Gap_and_Suggestion_Agent import create_research_gap_agent_task

from Config.shared import *

# Get user input at runtime
user_input = input("Enter your research field: ")

# Create the task using the dynamic input
trending_agent, trending_task = create_trending_topics_agent_task(user_input)

recent_papers_agent, recent_papers_task = create_recent_papers_agent_task()

research_gap_agent, research_gap_task = create_research_gap_agent_task()

# Create the crew with just this task
crew = Crew(
    agents=[trending_agent,
            recent_papers_agent,
            research_gap_agent,
            ],

    tasks=[trending_task,
           recent_papers_task,
           research_gap_task,
           ],

    verbose=True,
)

# Run the crew
crew.kickoff()
