from src.core.llm import llm
from src.core.parsers import analysis_parser, test_generation_parser, test_explanation_parser
from src.prompts.prompts import analysis_prompt, test_generation_prompt, explanation_prompt, chat_prompt
from src.memory.memory import get_session_history
from langchain_core.runnables.history import RunnableWithMessageHistory

# Chaîne 1 : Analyse de code
analysis_chain = (
    analysis_prompt.partial(format_instructions=analysis_parser.get_format_instructions())
    | llm
    | analysis_parser
)

# Chaîne 2 : Génération de test
test_generation_chain = (
    test_generation_prompt.partial(format_instructions=test_generation_parser.get_format_instructions())
    | llm
    | test_generation_parser
)

# Chaîne 3 : Explication de test
explanation_chain = (
    explanation_prompt.partial(format_instructions=test_explanation_parser.get_format_instructions())
    | llm
    | test_explanation_parser
)

# Chaîne 4 : Chat avec mémoire
base_chat = chat_prompt | llm

chat_chain = RunnableWithMessageHistory(
    base_chat,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)