# streamlit_app_2.py

import os
import json
import sys

# Set working directory
os.chdir("/home/israa/Desktop/PublishMate_CrewAgents")
sys.path.append("/home/israa/Desktop/PublishMate_CrewAgents")

import streamlit as st
from Config.shared import *
from agents.Trending_Topics_Agent import create_trending_topics_agent_task
from agents.Recent_Papers_Retrieval_Agent import create_recent_papers_agent_task
from agents.Research_Gap_and_Suggestion_Agent import create_research_gap_agent_task
from agents.Search_about_chosen_gab_Agent import create_research_starting_points_agent_task
from agents.Paper_Structure_and_Writing_Guide_Agent import create_paper_structure_agent_task
from agents.Related_work_draft_Agent import create_related_work_agent_task
from agents.Paper_draft_Agent import create_draft_writer_agent_task


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
    try:
        crew.kickoff()
        st.success("Task completed!")
    except Exception as e:
        st.error(f"Error running tasks: {e}")

st.title("Research AI Agents")

# Initialize session state for control flow
if "first_task_done" not in st.session_state:
    st.session_state.first_task_done = False
if "chosen_topic" not in st.session_state:
    st.session_state.chosen_topic = ""
if "chosen_gap" not in st.session_state:
    st.session_state.chosen_gap = ""

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

        st.write("### Trending Topics")
        for topic in trending_topics.get("topics", []):
            st.subheader(topic.get("name", "No Name"))
            st.write(topic.get("description", "No Description"))

        st.write("### Recent Papers")
        topic_papers = recent_papers.get("topic_papers", {})
        if topic_papers:
            for topic, papers in topic_papers.items():
                st.subheader(topic)
                for paper in papers:
                    st.markdown(f"**Title:** {paper.get('title', 'No Title')}")
                    st.markdown(f"**Year:** {paper.get('year', 'N/A')}")
                    st.markdown(f"**URL:** {paper.get('url', 'No URL')}")
                    st.markdown(f"**Abstract:** {paper.get('abstract', 'No Abstract')}")
                    st.write("---")
        else:
            st.info("No papers found, try again.")

        st.write("### Research Gaps")
        for gap in research_gaps.get("research_gaps", []):
            st.write(f"- {gap}")

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

            st.write("### Research Starting Points")
            steps = research_starting_points.get("research_steps", [])
            for idx, step in enumerate(steps, 1):
                st.subheader(f"{idx}. {step.get('section', 'No Section')}")
                st.write(step.get("tips", "No Tips"))

            st.write("### Paper Structure Guide")
            for section in paper_structure.get("paper_structure", []):
                st.subheader(section.get("section", "No Section"))
                st.write(section.get("tips", "No Tips"))

            st.write("### Related Work Draft")
            st.write(related_work.get("related_work", "No related work content."))

            st.write("### Paper Draft")
            st.write(draft.get("draft", "No draft content."))
