# PublishMate Crew Agents

Welcome to **PublishMate** 😊 — your AI-powered research assistant for academic paper writing! This project leverages multi-agent collaboration to guide researchers, especially beginners, through the entire academic paper workflow: from discovering trending topics to drafting a full paper.

---

## 🚀 Features

- **Trending Topics Discovery:** Find the latest hot topics in your research field.
- **Recent Papers Retrieval:** Get recent, reputable papers (with abstracts and links) for each trending topic.
- **Research Gap Analysis:** Identify gaps and suggestions for future research based on recent literature.
- **Research Starting Points:** Break down a chosen research gap into actionable, beginner-friendly steps.
- **Paper Structure Guide:** Generate a tailored academic paper outline with writing tips.
- **Related Work Drafting:** Compose a comprehensive related work section using real paper summaries.
- **Full Paper Drafting:** Automatically generate a full academic paper draft (Intro, Method, etc.) based on your chosen topic and gap.
- **(Optional) Paper Summarization:** Summarize papers into clear, concise paragraphs.
- **AgentOps Integration:** Monitor and analyze agent performance.

---

## 🗂️ Project Structure

```
PublishMate_CrewAgents/
├── Notebooks/
│   └── Project.ipynb      # Main Jupyter notebook (run this!)
├── .env                   # Your API keys (not included)
└── README.md              # This file
```

---

## 🛠️ Setup & Requirements

1. **Clone the repository** and navigate to the project folder.
2. **Install dependencies** (run in a notebook cell or terminal):

   ```bash
   pip install -U "crewai[tools,agentops]" python-dotenv gcloud google-genai tavily
   ```

3. **Set up your `.env` file** with the following keys:

   ```
   AGENTOPS_API_KEY=your_agentops_key
   GEMINI_API_KEY=your_gemini_key
   TAVILY_API_KEY=your_tavily_key
   ```

4. **Run `Project.ipynb`** in Jupyter or VS Code.

---

## 🧑‍💻 How It Works

1. **Start the notebook** and follow the prompts.
2. **Input your research field** — the agents will:
   - Find trending topics.
   - Retrieve recent papers for each topic.
   - Analyze research gaps.
3. **Choose a topic and gap** you want to explore.
4. **Get step-by-step research guidance, paper structure, related work, and a full draft.**
5. **(Optional)**: Use the summarization agent for concise paper summaries.

---

## 🤖 Agents Overview

- **Trending Topics Agent:** Finds hot topics in your field.
- **Recent Papers Agent:** Retrieves recent, reputable papers.
- **Research Gap Agent:** Identifies research gaps and suggestions.
- **Research Starting Points Agent:** Breaks down a gap into actionable steps.
- **Paper Structure Agent:** Outlines your paper and gives writing tips.
- **Related Work Agent:** Drafts the related work section.
- **Draft Writer Agent:** Generates a full academic paper draft.
- **(Optional) Paper Summarization Agent:** Summarizes papers.

---

## 📂 Output

All outputs (JSON files, drafts, etc.) are saved in the `PublishMate_agent_ouput` directory.

---

## 💡 Further Improvements

- Feedback system (like/dislike).
- Option to summarize using the whole paper.
- More advanced agent collaboration and monitoring.

---

## 📝 License

This project is for educational and research purposes.

---

## 🙏 Acknowledgements

- [CrewAI](https://github.com/joaomdmoura/crewai)
- [AgentOps](https://agentops.ai/)
- [Google Generative AI](https://ai.google.dev/)
- [Tavily](https://www.tavily.com/)

---

Happy researching with **PublishMate**! 🚀