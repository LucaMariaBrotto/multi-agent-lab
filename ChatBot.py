import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# The "Brain"
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini"
)

# The "System Prompt" (The Identity)
system_prompt = "You are a patient and helpful programming tutor. Explain concepts in a simple way."

# Testing the agent with a system message and a user message
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content="What is a variable in Python?")
]

print("The agent is thinking...")
response = model.invoke(messages)

print("\nAgent's Response:")
print(response.content)