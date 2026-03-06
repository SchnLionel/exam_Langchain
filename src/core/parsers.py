from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import PydanticOutputParser


# PARSER 1 : Pour l'analyse de code
# Le LLM doit retourner ces 3 informations
class CodeAnalysisOutput(BaseModel):
    is_optimal: bool = Field(description="True si le code est bon, False sinon")
    problems: List[str] = Field(description="Liste des problèmes trouvés")
    suggestions: List[str] = Field(description="Liste des suggestions d'amélioration")

# PARSER 2 : Pour la génération de test
class TestGenerationOutput(BaseModel):
    test_code: str = Field(description="Le code du test pytest généré")

# PARSER 3 : Pour l'explication de test
class TestExplanationOutput(BaseModel):
    explanation: str = Field(description="L'explication pédagogique du test")


# On crée les parsers LangChain à partir des modèles Pydantic
analysis_parser = PydanticOutputParser(pydantic_object=CodeAnalysisOutput)
test_generation_parser = PydanticOutputParser(pydantic_object=TestGenerationOutput)
test_explanation_parser = PydanticOutputParser(pydantic_object=TestExplanationOutput)