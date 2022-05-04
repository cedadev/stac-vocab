# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '17 Nov 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from abc import ABCMeta, abstractmethod
from configparser import ConfigParser
from typing import Optional

from pydantic import BaseModel

from rdflib import Graph, Literal, Namespace, RDF, SKOS


class CEDAConcept(BaseModel):
    """Common model for concept."""

    name: str
    pref_label: str

    definition: Optional[str]


class CEDASubScheme(BaseModel):
    """Common model for sub scheme."""

    namespace: str
    name: str


class CEDAConceptScheme(BaseModel):
    """Common model for concept scheme."""

    namespace: Optional[str]

    name: str
    pref_label: str

    alt_label: Optional[str]
    definition: Optional[str]

    concepts: Optional[list[CEDAConcept]]

    sub_schemes: Optional[list[CEDASubScheme]]


class BaseWorkflow(metaclass=ABCMeta):
    """ Base class for an executor """

    def __init__(self, conf, namespace, inputs, **kwargs):
        """ Constructor """
        ...

        self.conf = conf
        self.namespace = namespace
        self.inputs = self.INPUTS_CLASS(**inputs)

    @abstractmethod
    def run(self, conf: ConfigParser, command: str):
        """ Abstract method to run a command """
        ...

    @abstractmethod
    def parser(self, raw_concept_scheme: dict) -> CEDAConceptScheme:
        """ Abstract method to parse a vocab """
        ...

    def create_vocab(self, concept_schemes: list[CEDAConceptScheme]) -> None:
        """ method to create vocab """
        graph = Graph()
        graph.bind('skos', SKOS)

        namespace = Namespace(f"{self.namespace}:")

        for concept_scheme in concept_schemes:

            concept_scheme_uri = namespace[concept_scheme.name]

            graph.add((concept_scheme_uri, RDF.type, SKOS.ConceptScheme))
            graph.add((concept_scheme_uri, SKOS.prefLabel, Literal(concept_scheme.pref_label, lang='en')))

            if concept_scheme.definition:
                graph.add((concept_scheme_uri, SKOS.definition, Literal(concept_scheme.definition, lang='en')))

            if concept_scheme.alt_label:
                graph.add((concept_scheme_uri, SKOS.altLabel, Literal(concept_scheme.alt_label, lang='en')))

            if concept_scheme.concepts:
                for concept in concept_scheme.concepts:

                    concept_uri = namespace[concept.name]
    
                    graph.add((concept_uri, RDF.type, SKOS.Concept))
                    graph.add((concept_uri, SKOS.inScheme, concept_scheme_uri))
                    graph.add((concept_uri, SKOS.prefLabel, Literal(concept.pref_label, lang='en')))

                    if concept.definition:
                        graph.add((concept_uri, SKOS.definition, Literal(concept.definition, lang='en')))

            if concept_scheme.sub_schemes:
                for sub_scheme in concept_scheme.sub_schemes:

                    graph.parse(f"{self.conf['VOCAB']['cache_path']}/{sub_scheme.namespace}.xml")

                    sub_namespace =  Namespace(f"{sub_scheme.namespace}:")

                    graph.add((concept_scheme_uri, SKOS.narrower, sub_namespace[sub_scheme.name]))
                    graph.add((sub_namespace[sub_scheme.name], SKOS.broader, concept_scheme_uri))

        graph.serialize(destination=f"{self.conf['VOCAB']['cache_path']}/{self.namespace}.xml", format='xml')
