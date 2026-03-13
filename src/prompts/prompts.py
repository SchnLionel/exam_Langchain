from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Analyse de code Python
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un expert Python senior. Analyse le code fourni pour évaluer sa qualité, sa performance et sa lisibilité.
    Format de sortie : JSON pur uniquement (pas de balises markdown type ```json).
    {format_instructions}"""),
    ("human", "{input}")
])

# Génération de tests unitaires
test_generation_prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un expert en Quality Assurance (QA). 
    Génère un test unitaire robuste avec `pytest` couvrant les cas nominaux et les limites.
    Format de sortie : JSON pur uniquement (pas de balises markdown type ```json).
    {format_instructions}"""),
    ("human", "{input}")
])

# Explication de tests
explanation_prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un mentor Python. Explique le fonctionnement d'un test unitaire de manière pédagogique.
    Utilise des analogies si besoin et décompose chaque étape.
    Format de sortie : JSON pur uniquement (pas de balises markdown type ```json).
    {format_instructions}"""),
    ("human", "{input}")
])

# Chat libre avec historique
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Fournis des réponses précises et pédagogiques sur Python."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])