import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Charger les variables du fichier .env
load_dotenv()

# Récupérer la clé API depuis le .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Créer le modèle principal (LLaMA 70B)
primary_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

# Créer un modèle de fallback (LLaMA 8B)
fallback_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.2
)

# Utiliser le fallback en cas d'erreur (limites de débit, indisponibilité)
llm = primary_llm.with_fallbacks([fallback_llm])