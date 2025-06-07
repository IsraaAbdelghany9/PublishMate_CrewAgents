from Config.shared import *
from Config.llm import basic_llm
from Config.directories import *

class RelatedWorkOutput(BaseModel):
    related_work: str = Field(..., title="Composed related work section")

def create_related_work_agent_task(chosen_topic, chosen_gap):
    related_work_agent = Agent(
        role="Related Work Composer Agent",
        goal="\n".join([
            "Compose a comprehensive 'Related Work' section using the paper summaries.",
            "Group by themes, mention each paper's contribution.",
            "Maintain academic tone and cite like (e.g., 'Smith et al. 2023').",
            f"you have earlier the {chosen_topic} and {chosen_gap} related papers so you can write about them."

        ]),
        backstory="Helps users create strong literature review related content.",
        llm=basic_llm,
        verbose=True,
    )

    related_work_task = Task(
        description="\n".join([
            f"Input: list of paper summaries about {chosen_topic} in a {chosen_gap}.",
            "Group the papers realated from the recent paper agent and write a clear Related Work section.",
            "Use academic tone, smooth transitions, and citation style.",
            "Output a single string."
        ]),
        expected_output="Single string of the Related Work section.",
        output_json=RelatedWorkOutput,
        output_file=os.path.join(output_dir, "step_6_related_work.json"),
        agent=related_work_agent,
    )

    return related_work_agent, related_work_task