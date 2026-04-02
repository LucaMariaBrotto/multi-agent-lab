import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# Il "Cervello"
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini"
)

# Il "System Prompt" (L'identità)
system_prompt = "Sei un tutor di programmazione paziente e utile. Spiega i concetti in modo semplice."

# Test dell'agente con un messaggio di sistema e uno dell'utente
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content="Cos'è una variabile in Python?")
]

print("L'agente sta riflettendo...")
response = model.invoke(messages)

print("\nRisposta dell'Agente:")
print(response.content)