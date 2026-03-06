import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from src.core.chains import analysis_chain, test_generation_chain, explanation_chain, chat_chain
from src.memory.memory import get_user_history, store, get_session_history

load_dotenv()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/login")

AUTH_URL = os.getenv("AUTH_SERVICE_URL", "http://auth:8001")


# Modèles de données reçues dans les requêtes
class CodeInput(BaseModel):
    code: str

class TestInput(BaseModel):
    test_code: str

class ChatInput(BaseModel):
    message: str


# Fonction pour vérifier le token JWT auprès du service auth
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        response = httpx.get(f"{AUTH_URL}/me", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Token invalide")
        return response.json()["username"]
    except Exception:
        raise HTTPException(status_code=401, detail="Impossible de vérifier le token")


# Endpoint : Analyse de code
@app.post("/analyze")
def analyze(data: CodeInput, username: str = Depends(get_current_user)):
    result = analysis_chain.invoke({"input": data.code})
    # Sauvegarde dans la mémoire
    get_session_history(username).add_user_message(f"Analyse: {data.code}")
    get_session_history(username).add_ai_message(str(result.dict()))
    return result.dict()


# Endpoint : Génération de test
@app.post("/generate_test")
def generate_test(data: CodeInput, username: str = Depends(get_current_user)):
    result = test_generation_chain.invoke({"input": data.code})
    get_session_history(username).add_user_message(f"Génération test: {data.code}")
    get_session_history(username).add_ai_message(str(result.dict()))
    return result.dict()


# Endpoint : Explication de test
@app.post("/explain_test")
def explain_test(data: TestInput, username: str = Depends(get_current_user)):
    result = explanation_chain.invoke({"input": data.test_code})
    get_session_history(username).add_user_message(f"Explication: {data.test_code}")
    get_session_history(username).add_ai_message(str(result.dict()))
    return result.dict()


# Endpoint : Pipeline complet
@app.post("/full_pipeline")
def full_pipeline(data: CodeInput, username: str = Depends(get_current_user)):
    # Étape 1 : analyser le code
    analysis = analysis_chain.invoke({"input": data.code})

    # Si le code est non optimal, on s'arrête là
    if not analysis.is_optimal:
        return {"analysis": analysis.dict()}

    # Sinon, on génère un test puis on l'explique
    test = test_generation_chain.invoke({"input": data.code})
    explanation = explanation_chain.invoke({"input": test.test_code})

    # Sauvegarde dans la mémoire
    get_session_history(username).add_user_message(f"Full Pipeline: {data.code}")
    res_str = f"Analyse: {analysis.dict()}\nTest: {test.dict()}\nExplication: {explanation.dict()}"
    get_session_history(username).add_ai_message(res_str)

    return {
        "analysis": analysis.dict(),
        "test": test.dict(),
        "explanation": explanation.dict()
    }


# Endpoint : Console Interactive
@app.post("/chat")
def chat(data: ChatInput, username: str = Depends(get_current_user)):
    result = chat_chain.invoke(
        {"input": data.message},
        config={"configurable": {"session_id": username}}
    )
    return {"response": result.content}


# Endpoint : Historique
@app.get("/history")
def history(username: str = Depends(get_current_user)):
    return {"history": get_user_history(username)}