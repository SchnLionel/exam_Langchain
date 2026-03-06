from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# PROMPT 1 : Pour analyser du code Python
# {input} = le code envoyé par l'utilisateur
# {format_instructions} = les instructions pour répondre en JSON
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un expert Python. Analyse le code et réponds UNIQUEMENT en JSON.\n{format_instructions}"),
    ("human", "{input}")
])

# PROMPT 2 : Pour générer un test unitaire pytest
test_generation_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un expert en tests Python avec pytest. Génère un test unitaire et réponds UNIQUEMENT en JSON.\n{format_instructions}"),
    ("human", "{input}")
])

# PROMPT 3 : Pour expliquer un test à un débutant
explanation_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un professeur Python. Explique le test de façon simple pour un débutant et réponds UNIQUEMENT en JSON.\n{format_instructions}"),
    ("human", "{input}")
])

# PROMPT 4 : Pour le chat libre (avec mémoire des échanges précédents)
# MessagesPlaceholder("history") injecte les anciens messages dans la conversation
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Fournis des réponses précises et pédagogiques sur Python."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])