from Config.shared import *
from Config.llm import basic_llm
from Config.directories import *


class ResearchGapOutput(BaseModel):
    research_gaps: List[str] = Field(..., title="List of research gaps and suggestions")


def create_research_gap_agent_task():
    research_gap_agent = Agent(
        role="Research Gap Identification and Suggestion Agent",
        goal="\n".join([
            "Analyze summaries to identify gaps, limitations, and propose research directions or improvements.",
            "Use a friendly and encouraging tone suitable for beginners.",
            "You will be given data about papers on that topic — 3 papers per topic with their year, abstract, URL, and title.",
            "Analyze the abstracts to detect gaps.",
            "Suggest these gaps to help the writer start from them."
        ]),
        backstory="Helps users find novel contributions by highlighting unexplored areas and providing ideas.",
        llm=basic_llm,
        verbose=False,
    )

    research_gap_task = Task(
        description="\n".join([
            "Input is paper summaries.",
            "Output a list of research gaps, limitations, and suggestions for future research.",
            "Encourage beginners by providing feasible ideas.",
            "You will be given data about papers on that topic — 3 papers per topic with their year, abstract, URL, and title.",
            "Analyze the abstracts to detect gaps.",
            "Suggest these gaps to help the writer start from them."
        ]),
        expected_output="JSON list of research gaps and improvement suggestions.",
        output_json=ResearchGapOutput,
        output_file=os.path.join(output_dir, "step_3_research_gaps.json"),
        agent=research_gap_agent,
    )

    return research_gap_agent, research_gap_task
