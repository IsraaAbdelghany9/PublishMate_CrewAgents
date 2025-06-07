# main.py

from agents.Trending_Topics_Agent import create_trending_topics_agent_task
from agents.Recent_Papers_Retrieval_Agent import create_recent_papers_agent_task
from agents.Research_Gap_and_Suggestion_Agent import create_research_gap_agent_task
from agents.Search_about_chosen_gab_Agent import create_research_starting_points_agent_task
from Config.shared import *

# Get user input at runtime
user_input = input("Enter your research field: ")

# Create the task using the dynamic input
trending_agent, trending_task = create_trending_topics_agent_task(user_input)

recent_papers_agent, recent_papers_task = create_recent_papers_agent_task()

research_gap_agent, research_gap_task = create_research_gap_agent_task()

# Create the crew with just this task
crew1 = Crew(
    agents=[trending_agent,
            recent_papers_agent,
            research_gap_agent,
            ],

    tasks=[trending_task,
           recent_papers_task,
           research_gap_task,
           ],

    verbose=False,
)

# Run the crew
# crew.kickoff()

results = crew1.kickoff

## Read the output from the files


chosen_topic = input("Which topic did you get interested in more? ")
chosen_gap = input("Which gap do you like to start looking for ^-^? ")


research_starting_points_agent, research_starting_points_task = create_research_starting_points_agent_task(chosen_topic= chosen_topic, chosen_gap= chosen_gap)

crew2 = Crew(
    agents=[research_starting_points_agent,
            ],

    tasks=[research_starting_points_task,
           ],

    verbose=True,
)