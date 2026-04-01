import os
from dotenv import load_dotenv

# Agent tools
from langchain.agents import create_openai_tools_agent, AgentExecutor

# Modello LLM
from langchain_openai import ChatOpenAI

# Prompt (IMPORTANTISSIMO per gli agent)
from langchain_core.prompts import ChatPromptTemplate

# Tool decorator
from langchain_core.tools import tool


# 1. Carichiamo le variabili d'ambiente (.env)
# Necessario per non hardcodare API keys
load_dotenv()


# 2. Configuriamo il modello
# Usiamo OpenRouter come provider (compatibile OpenAI API)
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini",
    temperature=0.1,  # 👉 basso = più deterministico (meglio per tool)
    max_tokens=1000
)


# 3. Definizione TOOL
# Il decorator @tool permette al modello di "vedere" questa funzione
@tool
def multiply(a: int, b: int) -> int:
    """Moltiplica due numeri interi tra loro. Usalo per calcoli matematici."""
    return a * b

@tool
def calculator(expression: str) -> str:
    """Valuta un'espressione matematica (es: '2+3*4')."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Errore: {e}"
    

from datetime import datetime

@tool
def get_current_time() -> str:
    """Restituisce l'ora attuale."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def search_docs(query: str) -> str:
    """Cerca informazioni in una knowledge base interna."""
    
    docs = {
        "python": "Python è un linguaggio di programmazione.",
        "langchain": "LangChain è un framework per costruire applicazioni con LLM.",
        "ai agent": "Un AI agent usa tool per interagire con il mondo esterno."
    }
    
    for key in docs:
        if key in query.lower():
            return docs[key]
    
    return "Nessuna informazione trovata."

# Lista tool
# Gli agent lavorano sempre con liste di tool
tools = [multiply, calculator, get_current_time, search_docs]


# 4. Prompt strutturato (OBBLIGATORIO)
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "Sei un assistente intelligente che usa tool quando necessario. "
     "Per calcoli usa i tool matematici. "
     "Per informazioni usa search_docs. "
     "Non inventare risultati se puoi usare un tool."
     "Non mostrare il calcolo a mano, restituisci solo il risultato numerico."),
    
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])


# 5. Creazione AGENT
# Qui colleghiamo: modello + tool + prompt
agent = create_openai_tools_agent(
    model,
    tools,
    prompt
)


# 6. Agent Executor
# Questo è il "motore" che gestisce:
#    - chiamata LLM
#    - uso tool
#    - loop reasoning
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools
    # verbose=True  # utile per debug (vedi quando usa i tool)
)


# 7. Test
try:
    
    print("\nL'agente sta riflettendo...\n")

    response = agent_executor.invoke({

        # PER INSERIRE DOMANDE METTERE QUI    
        "input": "Quanto fa (23 * 45) + 12?, Che cos'è LangChain? E Che ore sono?"
    })
    print(response["output"])

except Exception as e:
    print(f"\nErrore: {e}")