# Currently applying the "Agents as Tools" Pattern
# In order to create a virtual environment, write in terminal: 
# python3 -m venv venv && source venv/bin/activate
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub # in order to download the prompt template from the hub
from rich.console import Console
from rich.markdown import Markdown

console = Console()

load_dotenv()

model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini",
)

# Create specialized logistics planning agent
@tool
def plan_logistics_agent(trip_request: str) -> str:
    """You are a travel logistics expert. You handle practical travel planning:
    - Calculate distances between locations and travel times
    - Estimate costs for transportation, accommodation, and activities
    - Optimize routes and suggest efficient itineraries
    - Consider time zones, weather, and practical constraints
    Always provide short, clear, practical logistics information."""
    
    return model.invoke(f"You are a logistics expert. Plan: {trip_request}").content

# Create specialized recommendations agent
@tool
def get_recommendations_agent(trip_details: str) -> str:
    """You are a travel recommendations specialist. You suggest experiences and activities:
    - Recommend top attractions, landmarks, and must-see places
    - Suggest restaurants, local cuisine, and dining experiences
    - Recommend cultural activities, events, and local experiences
    - Provide insights about local customs, best times to visit, and hidden gems
    Always provide brief, engaging, personalized recommendations."""
    return model.invoke(f"You are a recommendations expert. Suggest for: {trip_details}").content

# Create the orchestrator agent that combines both specialists

tools = [plan_logistics_agent, get_recommendations_agent]

prompt = hub.pull("hwchase17/openai-tools-agent")

agent = create_openai_tools_agent(model, tools, prompt)

# The AgentExecutor is what allows us to run the orchestrator agent with the tools.
# It will handle the logic of when to call each tool based on the prompt and the input.
orchestrator_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Test
# ... (keep all the initial part of imports, tools and orchestrator_executor definition)

print("-" * 50)
print("TRAVEL PLANNER AI - Terminal Mode")
print("Type your request and press ENTER to plan.")
print("-" * 50)

while True:
    # The program pauses here until you press Enter
    user_prompt = input("\nRequest > ")
    
    # If you press Enter without writing anything, the script ignores it and restarts
    if not user_prompt.strip():
        continue
        
    # We handle the exit only if you explicitly write something like 'exit' or 'quit'
    if user_prompt.lower() in ["exit", "quit"]:
        break

    print("\n[Thinking...]")
    
    try:
        response = orchestrator_executor.invoke({"input": user_prompt})
        
        # Create a Markdown object from the response text
        # This will remove the asterisks and convert them into visual formatting
        md = Markdown(response["output"])

        print("\n" + "─" * 30)
        console.print(md)
        print("─" * 30)
        
    except Exception as e:
        print(f"\nError during processing: {e}")