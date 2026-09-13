import os
from dotenv import load_dotenv

# Agent tools
from langchain.agents import create_openai_tools_agent, AgentExecutor

# LLM Model
from langchain_openai import ChatOpenAI

# Prompt (VERY IMPORTANT for agents)
from langchain_core.prompts import ChatPromptTemplate

# Tool decorator
from langchain_core.tools import tool


# 1. Load environment variables (.env)
# Necessary to avoid hardcoding API keys
load_dotenv()


# 2. Configure the model
# We use OpenRouter as a provider (OpenAI API compatible)
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini",
    temperature=0.1,  # low = more deterministic (better for tools)
    max_tokens=1000
)


# 3. TOOL definition
# The @tool decorator allows the model to "see" this function
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers. Use this for mathematical calculations."""
    return a * b

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression (e.g.: '2+3*4')."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"
    

from datetime import datetime

@tool
def get_current_time() -> str:
    """Returns the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def search_docs(query: str) -> str:
    """Searches for information in an internal knowledge base."""
    
    docs = {
        "python": "Python is a programming language.",
        "langchain": "LangChain is a framework for building applications with LLMs.",
        "ai agent": "An AI agent uses tools to interact with the outside world."
    }
    
    for key in docs:
        if key in query.lower():
            return docs[key]
    
    return "No information found."

# Tool list
# Agents always work with tool lists
tools = [multiply, calculator, get_current_time, search_docs]


# 4. Structured prompt (MANDATORY)
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an intelligent assistant that uses tools when necessary. "
     "Use mathematical tools for calculations. "
     "Use search_docs for information. "
     "Do not invent results if you can use a tool."
     "Do not show manual calculations, just return the numerical result."),
    
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])


# 5. AGENT creation
# Here we connect: model + tools + prompt
agent = create_openai_tools_agent(
    model,
    tools,
    prompt
)


# 6. Agent Executor
# This is the "engine" that manages:
#    - LLM calls
#    - tool usage
#    - reasoning loop
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools
    # verbose=True  # useful for debugging (see when it uses tools)
)


# 7. Test
try:
    
    print("\nThe agent is thinking...\n")

    response = agent_executor.invoke({

        # TO INSERT QUESTIONS PUT THEM HERE    
        "input": "What is (23 * 45) + 12?, What is LangChain? And what time is it?"
    })
    print(response["output"])

except Exception as e:
    print(f"\nError: {e}")