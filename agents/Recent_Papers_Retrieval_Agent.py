
from Config.shared import *
from Config.llm import basic_llm
from Tools.tavily_client import search_engine_tool 
from Config.directories import *

class PaperInfo(BaseModel):
    title: str  
    year: int 
    url: str
    abstract: str                                   

class RecentPapersOutput(BaseModel):
    topic_papers: Dict[str, List[PaperInfo]] = Field(..., title="Recent papers grouped by topic")

def create_recent_papers_agent_task():

    recent_papers_agent = Agent(
        role="Recent Papers Retrieval Agent",

        goal = "\n".join([
            "You are a research paper search assistant.",
            "Given a list of trending topics, retrieve 3 recent, relevant publications per topic.",
            "Select papers from reputable sources published within the last 2 years.(2023 or 2024 or 2025)",
            "Provide title, authors, abstract, year, and valid URL for each paper.",
            "the URL must be valid and accessible.",
            "If no recent paper is available, state 'No recent papers found' for that topic.",
            "Output in JSON format grouped by topic."]),

        backstory="Helps beginner researchers quickly discover and review the latest relevant publications across the trending topics with the URLs that are valid and some info.",

        llm=basic_llm,
        
        verbose=True,
    )

    recent_papers_task = Task(
        description="\n".join([
            "Input is a list of trending topics.",
            "For each topic, find 3 papers with title, authors, abstract, year, and link which should be valid and accessable.",
            "Select papers from reputable journals or conferences (IEEE, Springer, Elsevier, ICRA, IROS, actual arXiv).",
            "Only include papers published in 2023 or 2024 or 2025.",
            "Get the abstract of the paper as it is in the paper or the site to help the agents after you, bring a good clean text."
            "Focus on papers from last 2 years from reputable conferences or journals.",
            "If no recent paper is available, state 'No recent papers found' for that topic.",
            "Output JSON grouped by topic."
        ]),
        expected_output="JSON with topics as keys and list of paper info objects as values.",
        output_json=RecentPapersOutput,
        output_file=os.path.join(output_dir, "step_2_recent_papers.json"),
        agent=recent_papers_agent,
        tools=[search_engine_tool],
        
    )

    return recent_papers_agent, recent_papers_task
