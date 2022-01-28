

from pydantic import BaseModel
from yaml import safe_load
from typing import Dict, List

class SubScheme(BaseModel):
    name: str
    namespace: str

class ConceptSchemeConfig(BaseModel):
    name: str
    description: str
    sub_schemes: List[SubScheme]

class Concept(BaseModel):
    name: str
    location: str

class WorkflowConfig(BaseModel):
    concepts: List[Concept]

class Configuration(BaseModel):
    concept_schemes: List[ConceptSchemeConfig]
    workflows: Dict[str, WorkflowConfig]

    @classmethod
    def load_yaml(cls, filepath: str) -> None:
        """Loads a YAML config file."""
        with open(filepath) as reader:
            data = safe_load(reader)
        return cls.parse_obj(data)



