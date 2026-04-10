# Currently applying the "Agents as Tools" Pattern
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub # in order to download the prompt template from the hub

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
    
    return model.invoke(f"Sei un esperto di logistica. Pianifica: {trip_request}").content

# Create specialized recommendations agent
@tool
def get_recommendations_agent(trip_details: str) -> str:
    """You are a travel recommendations specialist. You suggest experiences and activities:
    - Recommend top attractions, landmarks, and must-see places
    - Suggest restaurants, local cuisine, and dining experiences
    - Recommend cultural activities, events, and local experiences
    - Provide insights about local customs, best times to visit, and hidden gems
    Always provide brief, engaging, personalized recommendations."""
    return model.invoke(f"Sei un esperto di raccomandazioni. Suggerisci per: {trip_details}").content

# Create the orchestrator agent that combines both specialists

tools = [plan_logistics_agent, get_recommendations_agent]

prompt = hub.pull("hwchase17/openai-tools-agent")

agent = create_openai_tools_agent(model, tools, prompt)

# L'AgentExecutor is what allows us to run the orchestrator agent with the tools.
# It will handle the logic of when to call each tool based on the prompt and the input.
orchestrator_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Test
response = orchestrator_executor.invoke({
    "input": "Plan a 3-day trip to Rome. I'm coming from London with a budget of $2000. Calculate travel costs and time, and suggest must-see attractions and restaurants."
})

print(response["output"])


