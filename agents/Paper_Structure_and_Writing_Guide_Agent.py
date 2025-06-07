

from Config.shared import *
from Config.llm import basic_llm
from Config.directories import *

# Input: specific research steps from previous agent
class ResearchGapSection(BaseModel):
    section: str
    tips: str

# Output: paper structure with tips for writing
class PaperStructureSection(BaseModel):
    section: str
    tips: str

class PaperStructureOutput(BaseModel):
    paper_structure: List[PaperStructureSection] = Field(..., title="Paper structure sections and writing tips")

def create_paper_structure_agent_task():
    paper_structure_agent = Agent(
        role="Paper Structure and Writing Guide Agent",
        goal="\n".join([
            "Take research steps as input and produce a paper outline that reflects them.",
            "For each section in the paper, provide clear writing tips tailored to the input research.",
            "Help beginners turn their research process into a coherent academic paper.",
            "Add encouragement and make the structure simple to follow."
        ]),
        backstory="Transforms research plans into a proper academic paper structure with beginner tips.",
        llm=basic_llm,
        verbose=True,
    )

    paper_structure_task = Task(
        description="\n".join([
            "Input: List of research steps (sections with tips) from a research gap agent.",
            "Output: Structured academic paper outline based on those steps.",
            "Include tips for writing each section clearly and effectively.",
            "Make it easy to follow for someone new to academic writing."
        ]),
        expected_output="JSON list of paper sections with writing advice.",
        output_json=PaperStructureOutput,
        output_file=os.path.join(output_dir, "step_5_paper_structure.json"),
        agent=paper_structure_agent,
    )

    return paper_structure_agent, paper_structure_task