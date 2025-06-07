import os
import json
import sys
import time
import streamlit as st
import requests

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
tool_output = "output/tool_output.json"


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

    /* Title style */
    h1 {
        color: #003366;
        text-align: center;
        font-weight: bold;
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

    /* Questions label color */
    label, .stTextInput > label, .stSelectbox > label {
        color: #003366;
        font-weight: 600;
    }

    /* Separator line */
    .section-separator {
        border-top: 2px solid #003366;
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

intro_prompt = ("Every great research journey starts with a good plan. I’m PublishMate, your assistant, dedicated to helping you find the latest trends, identify gaps, and organize your ideas. Let’s achieve your research goals together.")

st.markdown(f"<div class='intro-box'>{intro_prompt}</div>", unsafe_allow_html=True)

# Session state
if "first_task_done" not in st.session_state:
    st.session_state.first_task_done = False
if "chosen_topic" not in st.session_state:
    st.session_state.chosen_topic = ""
if "chosen_gap" not in st.session_state:
    st.session_state.chosen_gap = ""


st.markdown(
    """
    <style>
    label {
        background-color: #444444 !important;  /* dark gray background */
        color: white !important;                /* white text */
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 5px;
    }
    input, select, textarea {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
        border-radius: 4px;
        padding: 5px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
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
        tool_output_json = read_json_file(tool_output)
        
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

        # Check if any topic has papers
        has_papers = any(len(papers) > 0 for papers in topic_papers.values())

        if has_papers:
            for topic, papers in topic_papers.items():
                if papers:  # only print topics with papers
                    st.markdown(f"**{topic}**")
                    for paper in papers:
                        st.markdown(f"- **Title:** {paper.get('title', 'No Title')}")
                        st.markdown(f"  - **Year:** {paper.get('year', 'N/A')}")
                        st.markdown(f"  - **URL:** {paper.get('url', 'No URL')}")
                        st.markdown(f"  - **Abstract:** {paper.get('abstract', 'No Abstract')}")
                        st.markdown("---")
        else:
            output_tool_papers = tool_output_json.get("results", [])
            st.info("All Papers found:")

            for paper in output_tool_papers:
                st.markdown(f"- **Title:** {paper.get('title', 'No Title')}")
                st.markdown(f"  - **URL:** {paper.get('url', 'No URL')}")
                st.markdown(f"  - **Content:** {paper.get('content', 'No Content')}")
                st.markdown("---")


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
                for step in steps:
                    section = step.get("section", "")
                    tips = step.get("tips", "")
                    st.markdown(f"**{section}**")
                    st.markdown(f"{tips}")
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("No starting points found.")

            st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
            st.markdown("### Paper Structure Guide")
            if paper_structure.get("paper_structure"):
                st.markdown("<ul class='subtitles-list'>", unsafe_allow_html=True)
                for section in paper_structure.get("paper_structure", []):
                    st.markdown(f"<li><strong>{section.get('section', 'No Section')}</strong>: {section.get('tips', 'No Tips')}</li>", unsafe_allow_html=True)
                st.markdown("</ul>", unsafe_allow_html=True)
            else:
                st.info("No paper structure found.")

            st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
            st.markdown("### Related Work Draft")
            st.write(related_work.get("related_work", "No related work content."))

            st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
            st.markdown("### Paper Draft")
            st.write(draft.get("draft", "No draft content."))

#########################################################################################################################
        import re
        # Validate Gmail format
        def is_valid_email(email):
            return re.fullmatch(r'^[A-Za-z0-9._%+-]+@gmail\.com$', email) is not None
            
        # Add custom CSS for dark gray label and white input box
        st.markdown("""
            <style>
            label {
                background-color: #444 !important;
                color: white !important;
                padding: 5px 10px;
                border-radius: 5px;
                display: inline-block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            input, textarea {
                background-color: white !important;
                color: black !important;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
        st.markdown("## 📣 Feedback")

        name = st.text_input("Name")
        gmail = st.text_input("Gmail")
        feedback = st.text_area("What do you think about PublishMate?")


        if st.button("Submit Feedback"):
            if feedback.strip() == "":
                st.warning("Please write some feedback before submitting.")

            elif not is_valid_email(gmail):
                st.warning("Please write valid mail before submitting.")

            else:
                form_url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSdiaaP9YJemZqlKky8z109JcR7E34O6iatezaKPa1aHbbUAqg/formResponse"
                form_data = {
                    "entry.1318153724": name,       
                    "entry.1280693106": gmail,
                    "entry.1166678387": feedback,  
                }

                response = requests.post(form_url, data=form_data)
                
                if response.status_code == 200:
                    st.success("Thank you! Feedback submitted.")
                else:
                    st.warning("Failed to submit feedback. Try again.")



