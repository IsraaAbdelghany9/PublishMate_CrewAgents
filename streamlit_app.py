import streamlit as st
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process, LLM


load_dotenv()

st.set_page_config(page_title="PublishMate", page_icon="📚", layout="wide")
st.title("📚 PublishMate - Your Academic Research Assistant")

# Session state to keep inputs and outputs
if 'research_field' not in st.session_state:
    st.session_state.research_field = ""
if 'trending_output' not in st.session_state:
    st.session_state.trending_output = ""
if 'chosen_topic' not in st.session_state:
    st.session_state.chosen_topic = ""
if 'research_gap_output' not in st.session_state:
    st.session_state.research_gap_output = ""
if 'chosen_gap' not in st.session_state:
    st.session_state.chosen_gap = ""
if 'paper_structure_output' not in st.session_state:
    st.session_state.paper_structure_output = ""
if 'draft_output' not in st.session_state:
    st.session_state.draft_output = ""

# Initialize your agents here (replace basic_llm with actual LLM)
def initialize_agents():
    basic_llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.2,
    provider="google_ai_studio",
    api_key=os.environ["GEMINI_API_KEY"]
    )
  # Replace with your LLM initialization

    trending_agent = Agent(
        role="Trending Topics Identification Agent",
        goal="Identify latest trending topics in a given research field.",
        backstory="Provide relevant and current research topics.",
        llm=basic_llm,
        verbose=True,
    )
    research_gap_agent = Agent(
        role="Research Gap Identification Agent",
        goal="Identify research gaps and suggest improvements.",
        backstory="Find unexplored areas and suggest ideas.",
        llm=basic_llm,
        verbose=True,
    )
    research_steps_agent = Agent(
        role="Research Steps Agent",
        goal="Provide research steps based on gap.",
        backstory="Give actionable research points.",
        llm=basic_llm,
        verbose=True,
    )
    paper_structure_agent = Agent(
        role="Paper Structure Agent",
        goal="Generate paper structure from research steps.",
        backstory="Create outline with writing tips.",
        llm=basic_llm,
        verbose=True,
    )
    draft_agent = Agent(
        role="Draft Writing Agent",
        goal="Write full academic paper draft.",
        backstory="Create complete draft from structure.",
        llm=basic_llm,
        verbose=True,
    )
    return trending_agent, research_gap_agent, research_steps_agent, paper_structure_agent, draft_agent

def main():
    st.header("Step 1: Enter Research Field")
    st.session_state.research_field = st.text_input("Research Field:", st.session_state.research_field)

    if st.session_state.research_field:
        trending_agent, research_gap_agent, research_steps_agent, paper_structure_agent, draft_agent = initialize_agents()

        st.markdown("---")
        st.header("Step 2: Find Trending Topics")
        if st.button("Find Trending Topics"):
            with st.spinner("Getting trending topics..."):
                task = Task(
                    description=f"List 3-5 trending topics with descriptions in {st.session_state.research_field}",
                    expected_output="Text response",
                    agent=trending_agent,
                )
                crew = Crew(agents=[trending_agent], tasks=[task], process=Process.sequential)
                result = crew.kickoff()
                st.session_state.trending_output = str(result)

        if st.session_state.trending_output:
            st.text_area("Trending Topics Output:", st.session_state.trending_output, height=200)
            topics = [line.strip() for line in st.session_state.trending_output.split('\n') if line.strip()]
            st.session_state.chosen_topic = st.selectbox("Choose a topic to continue:", topics)

        if st.session_state.chosen_topic:
            st.markdown("---")
            st.header("Step 3: Identify Research Gaps")
            if st.button("Find Research Gaps"):
                with st.spinner("Finding research gaps..."):
                    task = Task(
                        description=f"Identify research gaps and suggestions for topic: {st.session_state.chosen_topic}",
                        expected_output="Text response",
                        agent=research_gap_agent,
                    )
                    crew = Crew(agents=[research_gap_agent], tasks=[task], process=Process.sequential)
                    result = crew.kickoff()
                    st.session_state.research_gap_output = str(result)

            if st.session_state.research_gap_output:
                st.text_area("Research Gaps Output:", st.session_state.research_gap_output, height=200)
                gaps = [line.strip() for line in st.session_state.research_gap_output.split('\n') if line.strip()]
                st.session_state.chosen_gap = st.selectbox("Choose a research gap:", gaps)

            if st.session_state.chosen_gap:
                st.markdown("---")
                st.header("Step 4: Generate Paper Structure")
                if st.button("Generate Paper Structure"):
                    with st.spinner("Generating paper structure..."):
                        # Research steps task (optional, you can combine with paper structure)
                        task = Task(
                            description=f"Provide research steps for gap: {st.session_state.chosen_gap}",
                            expected_output="Text response",
                            agent=research_steps_agent,
                        )
                        crew = Crew(agents=[research_steps_agent], tasks=[task], process=Process.sequential)
                        steps_result = crew.kickoff()

                        # Paper structure task
                        task2 = Task(
                            description=f"Generate paper structure based on research steps for gap: {st.session_state.chosen_gap}",
                            expected_output="Text response",
                            agent=paper_structure_agent,
                        )
                        crew2 = Crew(agents=[paper_structure_agent], tasks=[task2], process=Process.sequential)
                        structure_result = crew2.kickoff()

                        st.session_state.paper_structure_output = f"Research Steps:\n{steps_result}\n\nPaper Structure:\n{structure_result}"

                if st.session_state.paper_structure_output:
                    st.text_area("Paper Structure Output:", st.session_state.paper_structure_output, height=300)

                st.markdown("---")
                st.header("Step 5: Generate Paper Draft")
                if st.button("Generate Paper Draft"):
                    with st.spinner("Writing paper draft..."):
                        task = Task(
                            description=f"Write full academic paper draft for topic {st.session_state.chosen_topic} addressing gap {st.session_state.chosen_gap}",
                            expected_output="Text response",
                            agent=draft_agent,
                        )
                        crew = Crew(agents=[draft_agent], tasks=[task], process=Process.sequential)
                        result = crew.kickoff()
                        st.session_state.draft_output = str(result)

                if st.session_state.draft_output:
                    st.text_area("Paper Draft Output:", st.session_state.draft_output, height=600)

if __name__ == "__main__":
    main()


