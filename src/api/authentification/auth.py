import hashlib
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt

app = FastAPI()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
users_db = {}

class UserCreate(BaseModel):
    username: str
    password: str

# Hasher le mot de passe avec sha256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/signup")
def signup(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    users_db[user.username] = hash_password(user.password)
    return {"message": "Utilisateur créé avec succès"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user != hash_password(form_data.password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    token = jwt.encode({"sub": form_data.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload.get("sub")}
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide")