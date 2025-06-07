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

def initialize_agents():
    basic_llm = LLM(
        model="gemini/gemini-1.5-flash",
        temperature=0.2,
        provider="google_ai_studio",
        api_key=os.environ["GEMINI_API_KEY"]
    )

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

def parse_trending_topics(raw_output):
    # Example parsing - replace with actual logic if needed
    # Assume output format: numbered topics like "1. Topic Name"
    lines = raw_output.split('\n')
    topics = []
    current_topic = ""
    buffer = []
    for line in lines:
        if line.strip() == "":
            continue
        if line.strip()[0].isdigit() and '.' in line:
            if current_topic:
                topics.append({"title": current_topic, "details": "\n".join(buffer)})
            current_topic = line.split('.', 1)[1].strip()
            buffer = []
        else:
            buffer.append(line.strip())
    if current_topic:
        topics.append({"title": current_topic, "details": "\n".join(buffer)})
    return topics

def parse_research_gaps(raw_output):
    # Combine all gaps and suggestions into one string for single selection
    # Here, we return the whole output as one item
    return [raw_output.strip()]

def main():
    st.markdown('<h2 style="color: #4B8BBE;">Step 1: Enter Research Field</h2>', unsafe_allow_html=True)
    st.session_state.research_field = st.text_input("Research Field:", st.session_state.research_field)

    if st.session_state.research_field:
        trending_agent, research_gap_agent, research_steps_agent, paper_structure_agent, draft_agent = initialize_agents()

        st.markdown("---")
        st.markdown('<h2 style="color: #306998;">Step 2: Find Trending Topics</h2>', unsafe_allow_html=True)
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
            topics = parse_trending_topics(st.session_state.trending_output)
            topic_titles = [t['title'] for t in topics]

            st.text_area("Trending Topics Output:", st.session_state.trending_output, height=200)
            st.session_state.chosen_topic = st.selectbox(
                "Select the topic you want to work on:",
                topic_titles
            )

        if st.session_state.chosen_topic:
            st.markdown("---")
            st.markdown('<h2 style="color: #FFD43B;">Step 3: Identify Research Gaps</h2>', unsafe_allow_html=True)
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
                # Here we put all gaps and suggestions into one selection, no multiple lines
                gaps = parse_research_gaps(st.session_state.research_gap_output)
                st.text_area("Research Gaps Output:", st.session_state.research_gap_output, height=200)
                st.session_state.chosen_gap = st.selectbox(
                    "Select the research gap to focus on:",
                    gaps
                )

            if st.session_state.chosen_gap:
                st.markdown("---")
                st.markdown('<h2 style="color: #4CAF50;">Step 4: Generate Paper Structure</h2>', unsafe_allow_html=True)
                if st.button("Generate Paper Structure"):
                    with st.spinner("Generating paper structure..."):
                        task = Task(
                            description=f"Provide research steps for gap: {st.session_state.chosen_gap}",
                            expected_output="Text response",
                            agent=research_steps_agent,
                        )
                        crew = Crew(agents=[research_steps_agent], tasks=[task], process=Process.sequential)
                        steps_result = crew.kickoff()

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
                st.markdown('<h2 style="color: #FF6F61;">Step 5: Generate Paper Draft</h2>', unsafe_allow_html=True)
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
