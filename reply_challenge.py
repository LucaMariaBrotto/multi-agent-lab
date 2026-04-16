import os
from ulid import ULID
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langfuse import observe
from dotenv import load_dotenv

# ← CARICA LE VARIABILI SUBITO, PRIMA DI TUTTO
load_dotenv()

# Import librerie
from ulid import ULID
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langfuse import observe
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Configura il modello con le variabili d'ambiente
model = ChatOpenAI(
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1", 
    model="gpt-4o-mini",
    temperature=0,
)

# Configuro il client di Langfuse con le chiavi e l'host specifico per la challenge
langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host="https://challenges.reply.com/langfuse"
)

# Funzione per generare un session_id unico per ogni sessione della challenge
def generate_session_id():
    return f"{os.getenv('TEAM_NAME')}-{str(ULID())}" 

# Aggiungi istruzioni di sistema
    messages = [
        SystemMessage(content="Sei un assistente utile e conciso per una challenge AI."),
        HumanMessage(content=user_prompt)
    ]

@observe()
def execute_agent_task(session_id, user_prompt):
    # Collega il trace alla sessione della challenge
    langfuse_client.update_current_trace(session_id=session_id)
    
    # Inizializza il callback per LangChain
    handler = CallbackHandler()
    
    # Passa il handler nella configurazione di invoke
    response = model.invoke(
        [HumanMessage(content=user_prompt)], 
        config={"callbacks": [handler]}
    )
    return response.content

# ============================================================
# 🚀 ESECUZIONE PRINCIPALE
# ============================================================
if __name__ == "__main__":
    # Definisci le domande della challenge 
    questions = [
        "Ciao, come stai?",
        "Qual è la capitale della Francia?",
        "Spiegami brevemente cos'è l'intelligenza artificiale."
    ]

# Genera ID sessione univoco
session_id = generate_session_id()
print(f"🆔 Session ID: {session_id}")

# Esecuzione delle domande con tracciamento su Langfuse
for q in questions:
    execute_agent_task(session_id, q)

# Flush finale per inviare tutti i dati a Langfuse
langfuse_client.flush() # CRITICO: invia i dati pendenti prima di terminare il programma

print("\n Esecuzione completata! Controlla i trace su Langfuse.")