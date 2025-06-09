# 📚 PublishMate — Your Smart Research Assistant

PublishMate is an AI-powered academic assistant that guides you through the research process — from identifying trending topics to drafting your research paper.

[🔗 Live Demo](https://publishmatecrew.streamlit.app/)


## 🎥 Demo

A full walkthrough demo of **PublishMate** is available on LinkedIn.  
📺 [Watch the demo here](https://www.linkedin.com/posts/israa-abdelghany_publishmate-researchmadeeasy-academicwriting-activity-7337497387449339906-Lvnb?utm_source=share&utm_medium=member_desktop&rcm=ACoAADfttacBPXINTBQU4ldsesFAWvBJTRtiZ8U)


---

## 🚀 Features

- **Multi-agent architecture powered by CrewAI**
- **Streamlit interface for interactivity**
- **Topic discovery and research gap analysis**
- **Recent paper retrieval**
- **Paper structure guidance**
- **Related work drafting**
- **Final paper drafting**
- **User feedback submission**

---

## 👥 Crew Design

The system is divided into **two CrewAI crews** for flexibility and user-centric experience:

### 🧠 Crew 1 – Exploration Phase
- **Trending Topics Agent**: Detects hot topics in your research field.
- **Recent Papers Agent**: Fetches recent publications.
- **Research Gap Agent**: Identifies gaps in current literature.

### ✍️ Crew 2 – Drafting Phase
- **Starting Points Agent**: Suggests steps to begin research.
- **Paper Structure Agent**: Outlines paper format with section tips.
- **Related Work Agent**: Generates related work content.
- **Paper Draft Agent**: Creates a complete draft from insights.

> ✨ The split allows users to select a **preferred gap** before initiating the second phase — providing control and relevance to their writing journey.

---

## 🗂️ Project Structure

```bash
PublishMate_CrewAgents/
├── agents/                          # CrewAI agents
│   ├── Paper_draft_Agent.py
│   ├── Paper_Structure_and_Writing_Guide_Agent.py
│   ├── Recent_Papers_Retrieval_Agent.py
│   ├── Related_work_draft_Agent.py
│   ├── Research_Gap_and_Suggestion_Agent.py
│   ├── Search_about_chosen_gab_Agent.py
│   └── Trending_Topics_Agent.py
│
├── app/                             # Streamlit app entry
│   └── streamlit_app_2.py
│
├── Config/                          # Shared configs
│   ├── env.py
│   ├── llm.py
│   └── shared.py
│
├── Notebooks/
│   └── Project.ipynb                # Jupyter notebook for testing
│
├── PublishMate_agent_ouput/        # Agent outputs as JSON
│   ├── step_1_trending_topics.json
│   ├── step_2_recent_papers.json
│   ├── step_3_research_gaps.json
│   ├── step_4_research_starting_points.json
│   ├── step_5_paper_structure.json
│   ├── step_6_related_work.json
│   └── step_7_paper_draft.json
│
├── Tools/
│   └── tavily_client.py            # External tool integration
│
├── requirements.txt
├── packages.txt
├── runtime.txt
└── README.md
```

---


## 💻 Local Development

To run the app locally:

```bash
git clone https://github.com/IsraaAbdelghany9/PublishMate_CrewAgents.git
cd PublishMate_CrewAgents
pip install -r requirements.txt
streamlit run app/streamlit_app_2.py
```
---

## ☁️ Streamlit Cloud Deployment

The app is live and publicly available:  
🌐 [**Launch PublishMate**](https://publishmatecrew.streamlit.app/)

To deploy it yourself on **Streamlit Cloud**, ensure you include the following setup files.

---
## 📓 Notebook First Approach

The included `Project.ipynb` Jupyter notebook allows quick testing of agents and logic before full integration.  
This approach is ideal for early experimentation and debugging during development.

🧪 Additionally, it was added to offer beginners — or anyone excited about the project — an easy and intuitive way to explore the code and understand the process.
--- 
## 💬 Feedback Integration

PublishMate includes a feedback submission system to collect user input after generating research drafts.  
This can easily be extended to send responses to a database or Google Form for deeper analysis or follow-up.

---

## 📜 License

Licensed under the **Apache 2.0 License**.  
See the [LICENSE](./LICENSE) file for full terms.

---

## 🙌 Credits

Developed by **Israa Abdelghany**

Special thanks to:

- **CrewAI** – Orchestrating multi-agent systems  
- **Tavily** – Research API integration  
- **Streamlit** – Simplifying UI deployment  
- **AgentOps** – Monitoring and debugging agents
---
## 🤝 Contributions

Feel free to **fork**, ⭐ **star**, and submit **pull requests**.  
Ideas, suggestions, and bug reports are always welcome and appreciated!

---

## 🧠 Final Thoughts

**PublishMate** demonstrates the potential of **collaborative AI agents** in the academic space.  
From topic exploration to full paper generation, it helps researchers **write smarter, not harder**.

---

Thanks for you time ^_^
