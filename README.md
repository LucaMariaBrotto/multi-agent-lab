# 🤖 Multi-Agent Lab (`multi-agent-lab`)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-121212?style=for-the-badge&logo=chainlink)](https://www.langchain.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-API-00A67E?style=for-the-badge)](https://openrouter.ai/)

An experimental sandbox exploring **Large Language Model (LLM) orchestration**, **custom tool usage**, and **Multi-Agent Systems (MAS)** architectures using **LangChain** and Python.

This repository serves as a hands-on playground to design, test, and evaluate autonomous agent workflows, hierarchical agent delegation, and real-time tool calling.

---

## 🌟 Key Implementations & Architectures

### 1. 🛠️ Single Agent with Custom Tools (`Agent.py`)
An autonomous agent empowered with specialized Python functions using LangChain's `@tool` decorator:
- **Mathematical Evaluation:** Dynamic expression parsing and integer calculations.
- **Knowledge Base Search:** Querying mock internal documentation for domain-specific context.
- **Temporal Context:** Fetching current date and system time (`get_current_time`).
- **Autonomous Reasoning:** Utilizes `create_openai_tools_agent` and `AgentExecutor` to dynamically decide when to call tools vs. generating text responses.

### 2. 🏛️ Multi-Agent Orchestration:  *Agents as Tools* Pattern (`MultiAgentSystem.py`)
A hierarchical Multi-Agent framework designed for complex task decomposition and specialization:
- **Orchestrator Agent:** Master controller routing user requests to specialized domain experts.
- **Specialized Sub-Agents:**
  - **Logistics Agent:** Calculates travel routes, time constraints, and cost estimations.
  - **Recommendations Agent:** Generates personalized local attractions, dining, and cultural insights.
- **Interactive Terminal UI:** Built with `rich` for real-time Markdown rendering and execution feedback.

### 3. 💬 Foundations & System Prompt Engineering (`ChatBot.py`)
- Core messaging primitives (`SystemMessage`, `HumanMessage`).
- System persona enforcement, output formatting constraints, and context handling.

---

## 🛠️ Tech Stack

- **Core Language:** Python 3.10+
- **Orchestration Framework:** LangChain / LangChain Core / LangChain OpenAI
- **LLM Provider:** OpenRouter (GPT-4o-mini)
- **Terminal UI & Formatting:** Rich (Console & Markdown rendering)
- **Environment Management:** `python-dotenv`

---


## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables
Create a `.env` file in the root folder with your OpenRouter API key:
```bash
OPENROUTER_API_KEY=your_api_key_here
```

### 5. Run any script
```bash
python ChatBot.py
python Agent.py
python MultiAgentSystem.py
```

## 💡 Example Use Case (Multi-Agent System)

The `MultiAgentSystem.py` script powers an interactive **AI Travel Planner**. Given a request like *"Plan a 3-day trip to Rome on a budget,"* the orchestrator automatically figures out whether to consult:
- the **logistics agent**, for costs, routes, and timing, and/or
- the **recommendations agent**, for attractions, food, and local experiences

## 📄 License

This project is licensed under the [MIT License](LICENSE), so feel free to use, modify, and share it.
