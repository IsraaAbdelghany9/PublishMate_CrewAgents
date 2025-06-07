from Config.shared import *
from Config.llm import basic_llm
from Config.directories import *


class ResearchGapSection(BaseModel):
    section: str
    tips: str

class ResearchGapOutput(BaseModel):
    research_steps: List[ResearchGapSection] = Field(..., title="Research gap focused steps and tips")

def create_research_starting_points_agent_task(chosen_topic, chosen_gap):
    
    research_starting_points_agent = Agent(
        role="Research Gap Exploration Agent",
        goal="\n".join([
            f"Provide a detailed and clear set of specific research starting points based on the chosen {chosen_gap} in the {chosen_topic}.",
            "Include practical and beginner-friendly tips for each step to help users start their research.",
            "Focus on actionable tasks tied directly to the selected gap (e.g., watermarking, hallucination, bias).",
            "Motivate users by giving confidence and clear direction."
        ]),
        backstory="Helps users dive into LLM research by breaking down complex gaps into simple, actionable steps.",
        llm=basic_llm,
        verbose=True,
    )

    research_starting_points_task = Task(
        description="\n".join([
            f"Input: the chosen research gap {chosen_gap} in the topic {chosen_topic} .",
            "Output: a structured list of specific research steps with detailed tips for each step.",
            "Goal: help beginners understand what to do first, what resources to use, and how to progress in a steps."
        ]),
        expected_output="JSON list of steps with detailed beginner tips.",
        output_json=ResearchGapOutput,
        output_file=os.path.join(output_dir, "step_research_gap.json"),
        agent=research_starting_points_agent,
    )

    return research_starting_points_agent, research_starting_points_task