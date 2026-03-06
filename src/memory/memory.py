from langchain_community.chat_message_histories import ChatMessageHistory

# Dictionnaire global qui stocke l'historique de chaque utilisateur
# Clé = session_id (nom d'utilisateur), Valeur = historique des messages
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    # Si l'utilisateur n'a pas encore d'historique, on en crée un
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_user_history(session_id: str) -> list:
    # Retourne l'historique sous forme de liste de dicts
    if session_id not in store:
        return []
    messages = []
    for msg in store[session_id].messages:
        role = "human" if msg.type == "human" else "ai"
        messages.append({"role": role, "content": msg.content})
    return messages