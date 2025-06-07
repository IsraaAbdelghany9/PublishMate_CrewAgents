from Config.shared import *
from Config.llm import basic_llm
from Config.directories import *

class DraftOutput(BaseModel):
    draft: str = Field(..., title="Full academic paper draft text")

def create_draft_writer_agent_task(chosen_topic, chosen_gap):

    draft_writer_agent = Agent(
        role="Academic Paper Drafting Agent",
        goal="\n".join([
            f"Write a full academic paper draft using the structure, topic{chosen_topic}, research gap {chosen_gap}, and related work.",
            "Ensure clarity, academic tone, and smooth transitions.",
            "Support beginners by avoiding jargon and including helpful examples.",
        ]),
        backstory="Turns raw research insights into a complete paper draft.",
        llm=basic_llm,
        verbose=True,
    )

    draft_writer_task = Task(
        description="\n".join([
            f"Input is: topic{chosen_topic}, paper structure + tips and starting points + research gap {chosen_gap}  + related work.",
            "Use them to generate a coherent draft of the academic paper.",
            "Output in well-organized academic format (Intro, Method, etc.)."
        ]),
        expected_output="String containing the full paper draft.",
        output_json=DraftOutput,
        output_file=os.path.join(output_dir, "step_7_paper_draft.json"),
        agent=draft_writer_agent,
    )

    return draft_writer_agent, draft_writer_task