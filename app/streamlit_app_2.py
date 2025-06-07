import os
import json
import sys
import time
import streamlit as st

# Set working directory
os.chdir("/home/israa/Desktop/PublishMate_CrewAgents")
sys.path.append("/home/israa/Desktop/PublishMate_CrewAgents")

from Config.shared import *
from agents.Trending_Topics_Agent import create_trending_topics_agent_task
from agents.Recent_Papers_Retrieval_Agent import create_recent_papers_agent_task
from agents.Research_Gap_and_Suggestion_Agent import create_research_gap_agent_task
from agents.Search_about_chosen_gab_Agent import create_research_starting_points_agent_task
from agents.Paper_Structure_and_Writing_Guide_Agent import create_paper_structure_agent_task
from agents.Related_work_draft_Agent import create_related_work_agent_task
from agents.Paper_draft_Agent import create_draft_writer_agent_task

# Paths to JSON outputs
trending_topics_path = "PublishMate_agent_ouput/step_1_trending_topics.json"
recent_papers_path = "PublishMate_agent_ouput/step_2_recent_papers.json"
research_gaps_path = "PublishMate_agent_ouput/step_3_research_gaps.json"
research_starting_points_path = "PublishMate_agent_ouput/step_4_research_starting_points.json"
paper_structure_path = "PublishMate_agent_ouput/step_5_paper_structure.json"
related_work_path = "PublishMate_agent_ouput/step_6_related_work.json"
draft_path = "PublishMate_agent_ouput/step_7_paper_draft.json"

def read_json_file(filepath):
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
        else:
            st.warning(f"File not found: {filepath}")
            return {}
    except Exception as e:
        st.error(f"Error reading {filepath}: {e}")
        return {}

def run_crew(crew):
    with st.spinner("Running tasks, please wait..."):
        try:
            crew.kickoff()
        except Exception as e:
            st.error(f"Error running tasks: {e}")
            return

    progress_bar = st.progress(0)
    for percent in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent + 1)

    st.success("Task completed!")

# Custom styles
st.markdown(
    """
    <style>
    /* Gray background for entire page */
    .stApp {
        background-color: #f0f0f0;
    }

    /* Title style: dark red */
    h1 {
        color: #8B0000; /* dark red */
        text-align: center;
        font-weight: bold;
    }

    /* Make input and select boxes white background */
    input[type="text"], .stTextInput > div > input, .stSelectbox > div > div > div {
        background-color: white !important;
        color: black !important;
    }

    /* Smaller subtitles as list items */
    ul.subtitles-list {
        list-style-type: disc;
        padding-left: 20px;
        color: #222222;
        font-size: 18px;
        font-weight: 600;
    }
    ul.subtitles-list li {
        margin-bottom: 6px;
    }

    /* Questions label background dark gray and text color */
    label, .stTextInput > label, .stSelectbox > label {
        background-color: #333333; /* dark gray */
        color: #ffffff;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
    }

    /* Separator line */
    .section-separator {
        border-top: 2px solid #8B0000; /* dark red line */
        margin: 20px 0;
    }

    /* Light gray box for intro */
    .intro-box {
        background-color: #d9d9d9;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        color: #333333;
        margin-bottom: 25px;
        white-space: pre-line;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page title and intro
st.markdown(
    """
    <style>
    h1 {
        color: #C04040 !important;  /* medium red */
        text-align: center;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1>Welcome to Your Publish Mate 😊</h1>", unsafe_allow_html=True)

intro_prompt = (
"Every great research journey starts with a good plan. I’m PublishMate, your assistant, dedicated to helping you find the latest trends, identify gaps, and organize your ideas. Let’s achieve your research goals together."
)

st.markdown(f"<div class='intro-box'>{intro_prompt}</div>", unsafe_allow_html=True)

# Session state
if "first_task_done" not in st.session_state:
    st.session_state.first_task_done = False
if "chosen_topic" not in st.session_state:
    st.session_state.chosen_topic = ""
if "chosen_gap" not in st.session_state:
    st.session_state.chosen_gap = ""

# User input
research_field = st.text_input("Enter your research field:")

if research_field:
    trending_agent, trending_task = create_trending_topics_agent_task(research_field)
    recent_papers_agent, recent_papers_task = create_recent_papers_agent_task()
    research_gap_agent, research_gap_task = create_research_gap_agent_task()

    crew1 = Crew(
        agents=[trending_agent, recent_papers_agent, research_gap_agent],
        tasks=[trending_task, recent_papers_task, research_gap_task],
        verbose=True,
    )

    if not st.session_state.first_task_done:
        if st.button("Run initial research tasks"):
            run_crew(crew1)
            st.session_state.first_task_done = True

    if st.session_state.first_task_done:
        trending_topics = read_json_file(trending_topics_path)
        recent_papers = read_json_file(recent_papers_path)
        research_gaps = read_json_file(research_gaps_path)

        st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
        st.markdown("### Trending Topics")
        if trending_topics.get("topics"):
            st.markdown("<ul class='subtitles-list'>", unsafe_allow_html=True)
            for topic in trending_topics.get("topics", []):
                st.markdown(f"<li><strong>{topic.get('name', 'No Name')}</strong>: {topic.get('description', 'No Description')}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
        else:
            st.info("No trending topics found.")

        st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
        st.markdown("### Recent Papers")
        topic_papers = recent_papers.get("topic_papers", {})
        if topic_papers:
            for topic, papers in topic_papers.items():
                st.markdown(f"**{topic}**")
                for paper in papers:
                    st.markdown(f"- **Title:** {paper.get('title', 'No Title')}")
                    st.markdown(f"  - **Year:** {paper.get('year', 'N/A')}")
                    st.markdown(f"  - **URL:** {paper.get('url', 'No URL')}")
                    st.markdown(f"  - **Abstract:** {paper.get('abstract', 'No Abstract')}")
                    st.markdown("---")
        else:
            st.info("No papers found, try again.")

        st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
        st.markdown("### Research Gaps")
        if research_gaps.get("research_gaps"):
            st.markdown("<ul class='subtitles-list'>", unsafe_allow_html=True)
            for gap in research_gaps.get("research_gaps", []):
                st.markdown(f"<li>{gap}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
        else:
            st.info("No research gaps found.")

        topics_list = [t.get("name", "") for t in trending_topics.get("topics", [])]
        gaps_list = research_gaps.get("research_gaps", [])

        st.selectbox("Which topic interested you more?", options=topics_list, key="chosen_topic")
        st.selectbox("Which gap do you want to start with?", options=gaps_list, key="chosen_gap")

        if st.button("Run detailed research tasks"):
            chosen_topic = st.session_state.get("chosen_topic", "")
            chosen_gap = st.session_state.get("chosen_gap", "")

            research_starting_points_agent, research_starting_points_task = create_research_starting_points_agent_task(chosen_topic, chosen_gap)
            paper_structure_agent, paper_structure_task = create_paper_structure_agent_task()
            related_work_agent, related_work_task = create_related_work_agent_task(chosen_topic, chosen_gap)
            draft_writer_agent, draft_writer_task = create_draft_writer_agent_task(chosen_topic, chosen_gap)

            crew2 = Crew(
                agents=[research_starting_points_agent, paper_structure_agent, related_work_agent, draft_writer_agent],
                tasks=[research_starting_points_task, paper_structure_task, related_work_task, draft_writer_task],
                verbose=True,
            )

            run_crew(crew2)

            research_starting_points = read_json_file(research_starting_points_path)
            paper_structure = read_json_file(paper_structure_path)
            related_work = read_json_file(related_work_path)
            draft = read_json_file(draft_path)

            st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
            st.markdown("### Research Starting Points")
            steps = research_starting_points.get("research_steps", [])
            if steps:
                st.markdown("<ul class='subtitles-list'>", unsafe_allow_html=True)
                for idx, step in enumerate(steps, 1):
                    st.markdown(f"<li><strong>{idx}. {step}</strong></li>", unsafe_allow_html=True)
                st.markdown("</ul>", unsafe_allow_html=True)
            else:
                st.info("No starting points found.")

            st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
            st.markdown("### Paper Structure and Writing Guide")
            sections = paper_structure.get("sections", [])
            if sections:
                st.markdown("<ul class='subtitles-list'>", unsafe_allow_html=True)
                for section in sections:
                    st.markdown(f"<li><strong>{section}</strong></li>", unsafe_allow_html=True)
                st.markdown("</ul>", unsafe_allow_html=True)
            else:
                st.info("No paper structure found.")

            st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
            st.markdown("### Related Work Draft")
            related_work_text = related_work.get("related_work_text", "")
            if related_work_text:
                st.text_area("Related Work", related_work_text, height=200)
            else:
                st.info("No related work draft found.")

            st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
            st.markdown("### Paper Draft")
            draft_text = draft.get("paper_draft_text", "")
            if draft_text:
                st.text_area("Paper Draft", draft_text, height=300)
            else:
                st.info("No draft found.")
else:
    st.info("Please enter your research field to start.")
