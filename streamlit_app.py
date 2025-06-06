import streamlit as st
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process
from typing import List, Dict
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Streamlit UI setup
st.set_page_config(page_title="PublishMate", page_icon="📚", layout="wide")
st.title("📚 Welcome to PublishMate - Your Academic Research Assistant")

# Initialize session state
if 'research_field' not in st.session_state:
    st.session_state.research_field = None
if 'trending_topics' not in st.session_state:
    st.session_state.trending_topics = []
if 'chosen_topic' not in st.session_state:
    st.session_state.chosen_topic = None
if 'research_gaps' not in st.session_state:
    st.session_state.research_gaps = []
if 'chosen_gap' not in st.session_state:
    st.session_state.chosen_gap = None

# Model classes
class TrendingTopicsOutput(BaseModel):
    topics: List[Dict[str, str]] = Field(..., title="Trending topics with description", min_items=1)

class ResearchGapOutput(BaseModel):
    research_gaps: List[str] = Field(..., title="List of research gaps and suggestions")

class ResearchGapSection(BaseModel):
    section: str
    tips: str

class ResearchStepsOutput(BaseModel):
    research_steps: List[ResearchGapSection] = Field(..., title="Research gap focused steps and tips")

class PaperStructureSection(BaseModel):
    section: str
    tips: str

class PaperStructureOutput(BaseModel):
    paper_structure: List[PaperStructureSection] = Field(..., title="Paper structure sections and writing tips")

class DraftOutput(BaseModel):
    draft: str = Field(..., title="Full academic paper draft text")

# Initialize agents and tasks
def initialize_agents():
    # Basic LLM configuration (you might want to replace this with your actual LLM setup)
    basic_llm = None  # Replace with your actual LLM initialization
    
    # Agent 1: Trending Topics Agent
    trending_topics_agent = Agent(
        role="Trending Topics Identification Agent",
        goal=f"You are an expert research assistant that identifies the latest trending topics in a specified field.",
        backstory="Designed to guide users by providing the most relevant and current trending research topics.",
        llm=basic_llm,
        verbose=True,
    )
    
    # Agent 2: Research Gap Agent
    research_gap_agent = Agent(
        role="Research Gap Identification and Suggestion Agent",
        goal="Analyze summaries to identify gaps, limitations, and propose research directions or improvements.",
        backstory="Helps users find novel contributions by highlighting unexplored areas and providing ideas.",
        llm=basic_llm,
        verbose=True,
    )
    
    # Agent 3: Research Starting Points Agent
    research_starting_points_agent = Agent(
        role="Research Gap Exploration Agent",
        goal="Provide detailed and clear set of specific research starting points based on chosen gaps.",
        backstory="Helps users dive into research by breaking down complex gaps into simple, actionable steps.",
        llm=basic_llm,
        verbose=True,
    )
    
    # Agent 4: Paper Structure Agent
    paper_structure_agent = Agent(
        role="Paper Structure and Writing Guide Agent",
        goal="Take research steps as input and produce a paper outline that reflects them.",
        backstory="Transforms research plans into a proper academic paper structure with beginner tips.",
        llm=basic_llm,
        verbose=True,
    )
    
    # Agent 5: Draft Writer Agent
    draft_writer_agent = Agent(
        role="Academic Paper Drafting Agent",
        goal="Write a full academic paper draft using the structure and research content.",
        backstory="Turns raw research insights into a complete paper draft.",
        llm=basic_llm,
        verbose=True,
    )
    
    return (
        trending_topics_agent,
        research_gap_agent,
        research_starting_points_agent,
        paper_structure_agent,
        draft_writer_agent
    )

# Streamlit app flow
def main():
    st.sidebar.header("PublishMate Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Trending Topics", "Research Gaps", "Paper Structure", "Draft Paper"])
    
    if page == "Home":
        st.header("Welcome to PublishMate!")
        st.write("""
        This tool will guide you through the academic research process:
        1. Discover trending topics in your field
        2. Identify research gaps
        3. Get structured guidance for your paper
        4. Generate a draft of your research paper
        """)
        
        research_field = st.text_input("Enter your research field or keyword:")
        if research_field:
            st.session_state.research_field = research_field
            st.success(f"Research field set to: {research_field}")
            st.write("Navigate to 'Trending Topics' to continue.")
    
    elif page == "Trending Topics":
        if not st.session_state.research_field:
            st.warning("Please enter your research field on the Home page first.")
            return
            
        st.header(f"Trending Topics in {st.session_state.research_field}")
        
        if st.button("Find Trending Topics"):
            with st.spinner("Identifying trending topics..."):
                # Initialize agents
                (trending_topics_agent, _, _, _, _) = initialize_agents()
                
                # Create and execute task
                trending_topics_task = Task(
                    description=f"Provide a list of 3 to 5 trending topics in {st.session_state.research_field} with brief descriptions.",
                    expected_output="JSON object with list of trending topics and descriptions.",
                    output_json=TrendingTopicsOutput,
                    agent=trending_topics_agent,
                )
                
                crew = Crew(
                    agents=[trending_topics_agent],
                    tasks=[trending_topics_task],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                st.session_state.trending_topics = result.get("topics", [])
            
            if st.session_state.trending_topics:
                st.success("Found trending topics!")
                for i, topic in enumerate(st.session_state.trending_topics, 1):
                    st.subheader(f"{i}. {topic['name']}")
                    st.write(topic['description'])
                
                # Let user select a topic
                topic_names = [topic['name'] for topic in st.session_state.trending_topics]
                st.session_state.chosen_topic = st.selectbox(
                    "Which topic are you interested in?",
                    topic_names
                )
                
                st.write("Navigate to 'Research Gaps' to continue.")
    
    elif page == "Research Gaps":
        if not st.session_state.chosen_topic:
            st.warning("Please select a topic on the Trending Topics page first.")
            return
            
        st.header(f"Research Gaps in {st.session_state.chosen_topic}")
        
        if st.button("Identify Research Gaps"):
            with st.spinner("Analyzing research gaps..."):
                # Initialize agents
                (_, research_gap_agent, _, _, _) = initialize_agents()
                
                # Create and execute task
                research_gap_task = Task(
                    description=f"Identify research gaps in {st.session_state.chosen_topic}",
                    expected_output="List of research gaps and suggestions.",
                    output_json=ResearchGapOutput,
                    agent=research_gap_agent,
                )
                
                crew = Crew(
                    agents=[research_gap_agent],
                    tasks=[research_gap_task],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                st.session_state.research_gaps = result.get("research_gaps", [])
            
            if st.session_state.research_gaps:
                st.success("Found research gaps!")
                for i, gap in enumerate(st.session_state.research_gaps, 1):
                    st.subheader(f"Gap {i}")
                    st.write(gap)
                
                # Let user select a gap
                st.session_state.chosen_gap = st.selectbox(
                    "Which research gap would you like to explore?",
                    st.session_state.research_gaps
                )
                
                st.write("Navigate to 'Paper Structure' to continue.")
    
    elif page == "Paper Structure":
        if not st.session_state.chosen_gap:
            st.warning("Please select a research gap on the Research Gaps page first.")
            return
            
        st.header(f"Paper Structure for {st.session_state.chosen_topic}")
        st.subheader(f"Research Gap: {st.session_state.chosen_gap}")
        
        if st.button("Generate Paper Structure"):
            with st.spinner("Creating paper structure..."):
                # Initialize agents
                (_, _, research_starting_points_agent, paper_structure_agent, _) = initialize_agents()
                
                # Create and execute tasks
                research_starting_points_task = Task(
                    description=f"Provide research steps for addressing: {st.session_state.chosen_gap}",
                    expected_output="List of research steps with tips.",
                    output_json=ResearchStepsOutput,
                    agent=research_starting_points_agent,
                )
                
                paper_structure_task = Task(
                    description="Create a paper structure based on the research steps",
                    expected_output="Paper structure with writing tips.",
                    output_json=PaperStructureOutput,
                    agent=paper_structure_agent,
                )
                
                crew = Crew(
                    agents=[research_starting_points_agent, paper_structure_agent],
                    tasks=[research_starting_points_task, paper_structure_task],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                paper_structure = result.get("paper_structure", [])
            
            if paper_structure:
                st.success("Generated paper structure!")
                for section in paper_structure:
                    st.subheader(section['section'])
                    st.write(section['tips'])
                
                st.write("Navigate to 'Draft Paper' to generate a full draft.")
    
    elif page == "Draft Paper":
        if not st.session_state.chosen_gap:
            st.warning("Please complete the previous steps first.")
            return
            
        st.header(f"Paper Draft for {st.session_state.chosen_topic}")
        st.subheader(f"Research Gap: {st.session_state.chosen_gap}")
        
        if st.button("Generate Paper Draft"):
            with st.spinner("Writing paper draft..."):
                # Initialize agents
                (_, _, _, _, draft_writer_agent) = initialize_agents()
                
                # Create and execute task
                draft_writer_task = Task(
                    description=f"Write a full academic paper draft about {st.session_state.chosen_topic} addressing {st.session_state.chosen_gap}",
                    expected_output="Complete paper draft.",
                    output_json=DraftOutput,
                    agent=draft_writer_agent,
                )
                
                crew = Crew(
                    agents=[draft_writer_agent],
                    tasks=[draft_writer_task],
                    process=Process.sequential
                )
                
                result = crew.kickoff()
                draft = result.get("draft", "")
            
            if draft:
                st.success("Generated paper draft!")
                st.text_area("Your Paper Draft", draft, height=600)
                st.download_button(
                    label="Download Draft",
                    data=draft,
                    file_name=f"{st.session_state.chosen_topic.replace(' ', '_')}_draft.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()