# Outil de Test Automatisé Python

## 🚀 Démarrage rapide

### 1. Configurer le fichier `.env`

```env
GROQ_API_KEY=votre_clé_groq
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=votre_clé_langsmith
LANGCHAIN_PROJECT=examen_langchain
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### 2. Lancer le projet

```bash
make
```

### 3. Ports disponibles

| Service       | URL                         |
|---------------|-----------------------------|
| API Auth      | http://localhost:8001        |
| API Analyse   | http://localhost:8000        |
| Interface     | http://localhost:8501        |

### 4. Commandes Makefile

```bash
make         # Lance tous les services
make down    # Arrête tout
make logs    # Affiche les logs
make build   # Reconstruit les images
make clean   # Arrête et supprime les volumes
```

---

## 🧪 Tests des endpoints

### Inscription
```bash
curl -X POST http://localhost:8001/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret"}'
```

### Login (récupérer le token JWT)
```bash
curl -X POST http://localhost:8001/login \
  -d "username=alice&password=secret"
```

### Analyse de code
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a,b):\n  return a+b"}'
```

### Génération de test
```bash
curl -X POST http://localhost:8000/generate_test \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b):\n    return a + b"}'
```

### Explication de test
```bash
curl -X POST http://localhost:8000/explain_test \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"test_code": "def test_add():\n    assert add(1,2) == 3"}'
```

### Pipeline complet
```bash
curl -X POST http://localhost:8000/full_pipeline \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a: int, b: int) -> int:\n    return a + b"}'
```

### Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explique moi pytest"}'
```

### Historique
```bash
curl -X GET http://localhost:8000/history \
  -H "Authorization: Bearer <TOKEN>"
```

---

# Examen LangChain : Analyseur de Tests Unitaires Python

## Consignes générales

L’examen a pour objectif de développer un analyseur intelligent capable d’analyser du code Python, de générer automatiquement des tests unitaires avec pytest, et d’expliquer ces tests de manière pédagogique.

Pour y parvenir, vous devrez mettre en place une architecture complète combinant plusieurs outils : 

- **LangChain** pour gérer les chaînes, les prompts, les parsers et la mémoire
- **FastAPI** pour exposer les fonctionnalités à travers une API sécurisée
- **Docker** avec un **Makefile** afin de conteneuriser et d’orchestrer l’ensemble du projet. 
- Une interface utilisateur avec **Streamlit** peut être ajoutée en complément, mais elle reste OPTIONELLE.

Pour réaliser cet examen, un [répertoire GitHub](https://github.com/DataScientest/exam_Langchain) vous est mis à disposition. La première étape consiste à cloner ce dépôt sur votre machine afin de disposer de toute la structure de projet attendue (dossiers, fichiers de configuration, Makefile, etc.). 

Ce dépôt sert de squelette : il vous fournit l’architecture de base que vous devrez compléter en implémentant les différents composants (chaînes LangChain, parsers, mémoire, API, conteneurisation).

```txt
exam_Langchain/                     
├── .env                             # Variables d'environnement (clés API GROQ + LangSmith)
├── .python-version                  # Version de Python utilisée (ici 3.13)
├── pyproject.toml                   # Gestion des dépendances et configuration du projet
├── Makefile                         # Commandes pour build/up/down les conteneurs
├── docker-compose.yml               # Orchestration des services (auth, main, streamlit)
├── README.md                        # Documentation principale du projet
└── src/                             # Code source du projet
    ├── api/                         # Dossier regroupant les services API
    │   ├── authentification/        # Service d’authentification 
    │   │   ├── Dockerfile.auth      
    │   │   ├── requirements.txt     
    │   │   └── auth.py              # Code FastAPI pour gérer signup, login, me
    │   └── assistant/               # Service principal de l’analyseur LangChain
    │       ├── Dockerfile.main      
    │       ├── requirements.txt     
    │       └── main.py              # Code FastAPI pour analyse/génération/tests/chat
    ├── core/                        # Composants centraux LangChain
    │   ├── llm.py                   # Configuration du modèle de langage (LLM + fallback)
    │   ├── chains.py                # Définition des différentes chaînes (analyse, test, etc.)
    │   └── parsers.py               # Parsers Pydantic pour structurer les sorties du LLM
    ├── memory/                       
    │   └── memory.py                # Fonctions pour gérer l’historique multi-utilisateurs
    ├── prompts/                     
    │   └── prompts.py               # Prompts pour analyse, génération, explication, chat
    ├── Dockerfile.streamlit (optionnel)   # Dockerfile pour l’interface utilisateur Streamlit
    ├── requirements.txt (optionnel)       # Dépendances pour l’app Streamlit
    └── app.py (optionnel)                  # Application Streamlit pour interagir avec l’analyseur
```

L’ensemble des consignes décrites ci-dessous doit être suivi en vous appuyant sur cette structure déjà préparée, que vous enrichirez progressivement pour aboutir à un analyseur fonctionnel.

### Le LLM (``src/core/llm.py``)

Le cœur de l’analyseur repose sur le modèle de langage (LLM), qui est responsable de la génération et de l’interprétation des réponses. Ce fichier a pour rôle de configurer et d’initialiser le modèle choisi, ainsi que de prévoir une solution de repli en cas de problème.

L’implémentation doit inclure :

- **Un modèle principal** : c’est le modèle par défaut utilisé pour toutes les requêtes (par exemple un modèle Groq LLaMA 70B).
- **Une récupération des clés API**: les identifiants et paramètres sensibles doivent être stockés dans le fichier ``.env`` et récupérés dans le code via des variables d’environnement.

Cette couche d’abstraction permet de séparer clairement la logique métier (chaînes, prompts, parsers) de la configuration du modèle. Ainsi, il est facile de changer de fournisseur ou de modèle sans avoir à modifier l’ensemble du projet.

### Les Prompts (src/prompts/prompts.py)

Les prompts jouent un rôle central dans l’architecture, car ce sont eux qui définissent la manière dont le modèle doit raisonner et formuler ses réponses. Ils servent d’instructions claires et contraignantes au LLM pour garantir que les sorties soient exploitables.

Dans cet examen, vous devez **mettre en place différents prompts** correspondant aux fonctionnalités attendues de l’analyseur :

- **Prompt d’analyse de code** : Demande au LLM d’évaluer un extrait de code Python et de déterminer s’il est optimal. Le modèle doit identifier d’éventuels problèmes (lisibilité, performance, bonnes pratiques manquantes) et proposer des améliorations.
- **Prompt de génération de tests unitaires** : A partir d’une fonction Python donnée, l’analyseur doit produire un test unitaire en pytest. La consigne doit obliger le modèle à répondre avec un contenu structuré, afin de pouvoir extraire le code du test automatiquement.
- **Prompt d’explication de tests** : Explication pédagogique et détaillée d’un test unitaire. L’analyseur doit se comporter comme un professeur et rendre le test compréhensible pour un étudiant ou un développeur débutant.
- **Prompt de conversation libre** : Discussion naturelle avec l’utilisateur. Ce prompt doit être conçu pour fonctionner avec la mémoire conversationnelle, en intégrant l’historique des échanges afin de donner de la continuité au dialogue.

Chaque prompt doit être construit de façon à toujours produire une réponse en JSON valide, afin de pouvoir être interprétée par les parsers.

> ⚠️ **Attention** : veillez à bien intégrer les variables placeholders (**``{input}``**, **``{format_instructions}``**, etc.) pour que le modèle reçoive les bonnes informations. Pour le chat avec mémoire, l’utilisation de **``MessagesPlaceholder``** est obligatoire afin de transmettre correctement l’historique des conversations au LLM.

### Les Parsers (``src/core/parsers.py``)

Les parsers constituent une étape essentielle du projet : ils permettent de convertir les réponses brutes du modèle en objets structurés et exploitables. Comme le LLM renvoie du texte, il est indispensable de transformer ces sorties en formats clairs (par exemple JSON) pour pouvoir les manipuler dans l’API et la mémoire.

Chaque fonctionnalité de l’analyseur est associée à un parser dédié :

- **Parser d’analyse de code** : Transformer la réponse du modèle en un objet contenant trois informations clés : 
    - code optimal ou non
    - une liste des problèmes détectés
    - une liste des suggestions d’amélioration 
- **Parser de génération de tests**: Extraire du texte brut uniquement la partie correspondant au code du test unitaire en pytest, sous forme exploitable et directement exécutable.
- **Parser d’explication de tests** : Convertir la sortie du modèle en une explication claire et pédagogique, sous forme de texte structuré.

Ces parsers doivent être construits avec Pydantic, ce qui garantit :

- Une validation stricte du format attendu.
- La sérialisation facile en dictionnaires (``.dict()``) pour le retour dans les endpoints.
- Une robustesse accrue face aux erreurs de format du modèle.

### Les Chaînes (``src/core/chains.py``)

Les chaînes LangChain constituent le cœur logique de l’analyseur : elles orchestrent le flux d’information entre les prompts, le modèle de langage et les parsers. Chaque fonctionnalité repose sur une chaîne dédiée, qui définit clairement comment le LLM doit être sollicité et comment sa sortie doit être exploitée.

Vous devez mettre en place plusieurs chaînes :

- **Chaîne d’analyse de code** : Utilise le prompt d’analyse, envoie la requête au LLM, puis parse la réponse pour obtenir un objet structuré contenant l’évaluation (optimalité, problèmes, suggestions).
- **Chaîne de génération de tests unitaires** : Prend en entrée une fonction Python et renvoie un test unitaire au format pytest. 
- **Chaîne d’explication de tests** : Transforme un test Python en une explication claire et pédagogique destinée à un utilisateur humain.
- **Chaîne de chat libre** : Permet une conversation libre. Contrairement aux autres chaînes, elle ne passe pas par un parser mais doit intégrer la mémoire pour assurer une continuité dans les échanges.

Chaque chaîne doit être construite de manière simple et modulaire, afin que l’API puisse les invoquer directement sans logique supplémentaire.

### La Mémoire (``src/memory/memory.py``)

La mémoire doit être implémentée de manière à gérer plusieurs utilisateurs en parallèle. L’idée est de disposer d’un store global qui associe chaque **session_id** à un historique de type ``InMemoryChatMessageHistory``.

Deux fonctions principales doivent être codées :

- **``get_session_history(session_id)``** : Retourne l’historique de la session pour un utilisateur donné. Si aucune session n’existe encore pour cet utilisateur, une nouvelle instance d’historique doit être créée automatiquement.
- **``get_user_history(session_id)``** : Permet de récupérer l’ensemble de l’historique de l’utilisateur sous forme de liste de dictionnaires, avec pour chaque message le rôle (human ou ai) et le contenu.

> ⚠️ Points importants à respecter :
>
> - Le session_id doit être unique par utilisateur (exemple : le nom d’utilisateur renvoyé par le JWT).
> - La mémoire est non persistante : elle sera réinitialisée si l’application est relancée.
> - Ce système doit être utilisé en particulier dans la chaîne de chat, avec ``RunnableWithMessageHistory``, pour assurer la continuité des conversations.

### Les APIs (``src/api/``)

L'examen se repose sur deux APIs distinctes, toutes deux développées avec FastAPI et exécutées dans des conteneurs séparés :

#### L’API d’authentification (``src/api/authentification/``)

Cette API est dédiée à la gestion de la sécurité et des utilisateurs. Elle doit permettre :

- **L’inscription (signup)** : créer un nouvel utilisateur et l’enregistrer dans une base (ici simulée par une structure interne).
- **La connexion (login)** : vérifier les identifiants permettant d’accéder aux autres services.

Chaque endpoint doit être protégé et renvoyer des erreurs claires en cas de problème (utilisateur existant, identifiants incorrects). Le service dispose de son propre Dockerfile et de dépendances spécifiques.

#### L’API principale (``src/api/assistant/``)

Cette API constitue le cœur de l’analyseur. Elle doit exposer plusieurs endpoints permettant d’interagir avec les chaînes LangChain définies dans ``src/core/``. Les fonctionnalités attendues sont :

- **Analyser un code Python (``/analyze``)** : Invoque la chaîne d’analyse et retourne l’évaluation du code.
- **Générer un test unitaire (``/generate_test``)** : Appelle la chaîne de génération pour produire un test en pytest.
- **Expliquer un test (``/explain_test``)** : Utilise la chaîne d’explication pour fournir une version pédagogique.
- **Exécuter le pipeline complet (``/full_pipeline``)** : Cet endpoint combine plusieurs étapes en une seule requête. Le code soumis est d’abord analysé par la chaîne d’analyse.
    - Si le résultat de l’analyse indique que le **code est non optimal**, le pipeline s’arrête immédiatement et l’API renvoie uniquement l’évaluation du code avec la liste des problèmes détectés et les suggestions d’amélioration.
    - En revanche, si l’analyse conclut que le **code est optimal**, alors le pipeline poursuit automatiquement les étapes suivantes : génération d’un test unitaire puis explication pédagogique du test.

- **Chat conversationnel (``/chat``)** : Permet une discussion libre avec mémoire, en utilisant ``RunnableWithMessageHistory``.
- **Historique (``/history``)** : Retourne l’ensemble des échanges pour un utilisateur.

> ⚠️ ***POINTS D'ATTENTION*** ⚠️ 
>
> - Les résultats des endpoints **``/analyze``**, **``/generate_test``**, **``/explain_test``** et **``/full_pipeline``** doivent être **enregistrés dans la mémoire associée à l’utilisateur**, afin que chaque interaction soit conservée dans son historique.
> - Les deux APIs doivent tourner dans **des conteneurs distincts (auth_service et assistant_service)**.
> - **L’API principale dépend de l’API d’authentification** pour vérifier l’identité des utilisateurs.
> - Une gestion rigoureuse des erreurs est indispensable : toutes les exceptions doivent être capturées et transformées en réponses HTTP explicites.

### Suivi et Monitoring avec LangSmith 

Pour améliorer la traçabilité et le suivi de l’analyseur, il est nécessaire d’intégrer LangSmith, la plateforme de monitoring et de debug pour LangChain. 

- Tracer toutes les requêtes envoyées au LLM, avec leur prompt et leur réponse.
- Visualiser les chaînes et leurs étapes (prompts, parsers, mémoire) dans une interface graphique.
- Déboguer plus facilement en cas de problème de format ou d’erreur du modèle.
- Comparer plusieurs versions de prompts ou de chaînes afin d’optimiser les performances de l’analyseur.

Pour activer LangSmith, vous devez configurer vos variables d’environnement dans le fichier ``.env``.

### Interface Streamlit 

En plus des APIs, vous pouvez proposer une interface utilisateur développée avec Streamlit. Elle rend l’analyseur beaucoup plus accessible et agréable à tester, en offrant une interaction directe sans passer par des requêtes API manuelles.

**Fonctionnalités attendues**

- Authentification et Connexion
- **Analyse** : Saisir un extrait de code Python et afficher le diagnostic du LLM
- **Génération de tests** : Fournir une fonction Python et obtenir automatiquement un test unitaire en pytest.
- **Explication de tests** : Coller un test unitaire et recevoir une explication détaillée et pédagogique.
- **Pipeline complet** : Exécuter en une seule fois l’analyse → génération → explication.
- **Console Interactive** : Discuter avec l’analyseur de manière naturelle, en utilisant la mémoire conversationnelle.
- **Historique** : Visualiser toutes les interactions de la session en cours.

### Déploiement avec Docker et Makefile

L’ensemble du projet doit être entièrement conteneurisé afin de garantir une mise en place simple, reproductible et indépendante de l’environnement de développement. 

**Services attendus**

- **auth** : l’API d’authentification, responsable de la gestion des utilisateurs
- **main** : l’API principale, qui expose les fonctionnalités LangChain (analyse, génération de tests, explication, pipeline, chat, historique).
- **streamlit** : l’interface utilisateur, permettant de tester facilement l’analyseur via une interface graphique.

Chaque service dispose de son propre **Dockerfile** et d’un fichier **requirements.txt** spécifique.

**Makefile**

Le Makefile doit centraliser toutes les commandes utiles au projet. le déploiement complet du projet ne doit nécessiter qu’une seule commande :

```bash
make
```

> ⚠️ POINTS D'ATTENTION ⚠️
>
> - Les ports doivent être exposés clairement et documentés dans le README.
> - Assurez-vous que toutes les variables sensibles (clés API, configuration LangSmith, etc.) soient bien stockées dans le fichier ``.env`` et chargées par **docker-compose**.

### README.md 

Votre projet doit obligatoirement contenir un fichier **README.md** clair et structuré.
Ce document doit expliquer le fonctionnement global de votre analyseur, ainsi que la manière de le déployer et de le tester.

- Étapes pour configurer ``.env``.
- Commandes principales du Makefile (make up, make down, make logs).
- Liste des endpoints disponibles et des ports (API auth et API analyseur).

**Tests**

Instructions pour vérifier que l’API fonctionne correctement (scénarios de test à réaliser) :

- inscription
- login
- analyse
- génération de test
- explication
- pipeline complet
- chat avec mémoire
- affichage historique


## Rappels et Conseils

Avant de commencer, gardez en tête les points suivants :

- **Organisation** : Respectez scrupuleusement la structure de projet fournie. Chaque fichier a un rôle précis (LLM, prompts, parsers, mémoire, API, etc.). Une bonne organisation facilitera la correction et la lecture de votre code.
- **Variables d’environnement** : Ne mettez jamais vos clés en clair dans le code. Stockez-les dans le fichier ``.env``.
- **Prompts** : Assurez-vous toujours d’utiliser les placeholders (**``{input}``**, **``{format_instructions}``**, etc.) et, pour le chat, le **MessagesPlaceholder** afin de bien gérer l’historique des échanges.
- **Parsers** : Imposez toujours un retour au format JSON. C’est ce qui garantit que vos endpoints renverront des objets structurés et exploitables.
- **Mémoire** : Utilisez un ``session_id`` unique pour éviter de mélanger les historiques. N’oubliez pas que la mémoire est en RAM et disparaît si vous redémarrez vos services.
- L’API d’authentification doit être séparée de l’API principale.
- **Docker** : Ne mettez dans vos Dockerfiles que ce qui est nécessaire. Copiez uniquement les fichiers utiles et exposez les bons ports.
- **README** : Ce fichier doit être écrit comme si un correcteur n’avait aucune connaissance préalable de votre projet. Indiquez clairement comment lancer les services, et comment tester chaque endpoint.
- **Tests** : prenez le temps de tester toutes les fonctionnalités (auth, analyse, génération, explication, pipeline, chat, historique). N’attendez pas la fin pour vérifier : testez au fur et à mesure.

> ⚠️ ASTUCE ⚠️
>
> - Créez un environnement virtuel ``uv`` avant de commencer à conteneuriser votre projet.
> - Dès que vous mettez en place une nouvelle chaîne, créez immédiatement son endpoint correspondant et testez-le pour vérifier son bon fonctionnement.

## Rendus

N'oubliez pas d'uploader votre examen sous le format d'une archive zip ou tar, dans l'onglet **Mes Exams**, après avoir validé tous les exercices du module.

> ⚠️ **IMPORTANT** ⚠️ : N’envoyez pas votre environnement virtuel (par ex. .venv ou uv) dans votre rendu. En cas de non-respect de cette consigne, un **repass automatique** de l’examen vous sera attribué.

Félicitations, si vous avez atteint ce point, vous avez terminé le module sur LangChain et LLM Experimentation ! 🎉.


