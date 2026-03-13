import streamlit as st
import requests

import os

API_AUTH = os.getenv("API_AUTH_URL", "http://auth:8001")
API_MAIN = os.getenv("API_MAIN_URL", "http://main:8000")

st.title("Outil de Test Python")

# ── Authentification ─────────────────────────────────────────────────────────
st.sidebar.header("Connexion")
username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

if st.sidebar.button("S'inscrire"):
    r = requests.post(f"{API_AUTH}/signup", json={"username": username, "password": password})
    st.sidebar.success(r.json().get("message", r.text))

token = None
if st.sidebar.button("Se connecter"):
    r = requests.post(f"{API_AUTH}/login", data={"username": username, "password": password})
    if r.status_code == 200:
        token = r.json()["access_token"]
        st.session_state["token"] = token
        st.sidebar.success("Connecté !")
    else:
        st.sidebar.error("Identifiants incorrects")

# Récupération du token depuis la session
token = st.session_state.get("token")
headers = {"Authorization": f"Bearer {token}"} if token else {}

# ── Onglets ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Analyse", "Générer Test", "Expliquer Test", "Pipeline Complet", "Chat", "Historique"
])

# Tab 1 : Analyse de code
with tab1:
    st.subheader("Analyser du code Python")
    code = st.text_area("Collez votre code ici")
    if st.button("Analyser"):
        r = requests.post(f"{API_MAIN}/analyze", json={"code": code}, headers=headers)
        st.json(r.json())

# Tab 2 : Génération de test
with tab2:
    st.subheader("Générer un test unitaire")
    code = st.text_area("Collez votre fonction ici")
    if st.button("Générer le test"):
        r = requests.post(f"{API_MAIN}/generate_test", json={"code": code}, headers=headers)
        st.code(r.json().get("test_code", ""), language="python")

# Tab 3 : Explication de test
with tab3:
    st.subheader("Expliquer un test unitaire")
    test_code = st.text_area("Collez votre test pytest ici")
    if st.button("Expliquer"):
        r = requests.post(f"{API_MAIN}/explain_test", json={"test_code": test_code}, headers=headers)
        st.write(r.json().get("explanation", ""))

# Tab 4 : Pipeline complet
with tab4:
    st.subheader("Pipeline complet (analyse → test → explication)")
    code = st.text_area("Collez votre code ici", key="pipeline")
    if st.button("Lancer le pipeline"):
        r = requests.post(f"{API_MAIN}/full_pipeline", json={"code": code}, headers=headers)
        st.json(r.json())

# Tab 5 : Chat
with tab5:
    st.subheader("Chat avec l'assistant")
    message = st.text_input("Votre message")
    if st.button("Envoyer"):
        r = requests.post(f"{API_MAIN}/chat", json={"message": message}, headers=headers)
        st.write(r.json().get("response", ""))

# Tab 6 : Historique
with tab6:
    st.subheader("Historique de la session")
    if st.button("Afficher l'historique"):
        r = requests.get(f"{API_MAIN}/history", headers=headers)
        for msg in r.json().get("history", []):
            st.write(f"**{msg['role']}**: {msg['content']}")