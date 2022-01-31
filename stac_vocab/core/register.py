# encoding: utf-8
"""
Code snippet taken from: https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe
"""
__author__ = 'Richard Smith'
__date__ = '17 Nov 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Standard imports
from abc import ABCMeta, abstractmethod
import logging
import json
from glob import glob
from typing import Callable
from ..sources.base import BaseWorkflow
from rdflib import Graph, Literal, Namespace, RDF, SKOS

logger = logging.getLogger(__name__)


class WorkflowFactory:
    """ The factory class for creating workflows"""

    registry = {}
    """ Internal registry for available workflows """

    @classmethod
    def register(cls, name: str) -> Callable:
        """ Class method to register workflow class to the internal registry.
        Args:
            name (str): The name of the workflow.
        Returns:
            The workflow class itself.
        """

        def inner_wrapper(wrapped_class: BaseWorkflow) -> Callable:
            if name in cls.registry:
                logger.warning('workflow %s already exists. Will replace it', name)
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    # end register()

    @classmethod
    def create_workflow(cls, name: str, **kwargs) -> 'BaseWorkflow':
        """ Factory command to create the workflow.
        This method gets the appropriate workflow class from the registry
        and creates an instance of it, while passing in the parameters
        given in ``kwargs``.
        Args:
            name (str): The name of the workflow to create.
        Returns:
            An instance of the workflow that is created.
        """

        if name not in cls.registry:
            logger.warning('workflow %s does not exist in the registry', name)
            return None

        exec_class = cls.registry[name]
        workflow = exec_class(**kwargs)
        return workflow


@WorkflowFactory.register('cmip6')
class Cmip6Workflow(BaseWorkflow):
    """? or importer class see. cmip5"""


    def create_vocab(self, config):
        graph = Graph()
        graph.bind('skos', SKOS)
        namespace = Namespace("http://test.org/cmip6/")
        for concept_scheme in config["concept_schemes"]:
            with open(concept_scheme["location"]) as f:
                facets = json.load(f)
                concept_scheme_uri = namespace[concept_scheme["name"]]
                graph.add((concept_scheme_uri, RDF.type, SKOS.ConceptScheme))
                graph.add((concept_scheme_uri, SKOS.prefLabel, Literal(concept_scheme["prefLabel"], lang='en')))

                if "altLabel" in concept_scheme.keys():
                    graph.add((concept_scheme_uri, SKOS.altLabel, Literal(concept_scheme["altLabel"], lang='en')))

            for key, concept in facets[concept_scheme["name"]].items():
                if isinstance(concept, str):
                    concept_uri = namespace[key]
                    graph.add((concept_uri, RDF.type, SKOS.Concept))
                    graph.add((concept_uri, SKOS.inScheme, concept_scheme_uri))
                    graph.add((concept_uri, SKOS.prefLabel, Literal(key, lang='en')))
                    graph.add((concept_uri, SKOS.definition, Literal(concept, lang='en')))

                else:
                    concept_uri = namespace[key]
                    graph.add((concept_uri, RDF.type, SKOS.Concept))
                    graph.add((concept_uri, SKOS.inScheme, concept_scheme_uri))
                    
                    if "label" in concept.keys():
                        graph.add((concept_uri, SKOS.prefLabel, Literal(concept["label"], lang='en')))
                    else:
                        graph.add((concept_uri, SKOS.prefLabel, Literal(key, lang='en')))
                    
                    if "label_extended" in concept.keys():
                        graph.add((concept_uri, SKOS.definition, Literal(concept["label_extended"], lang='en')))
                    
        return graph

    def run(self, config):
        vocab = self.create_vocab(config)

        return vocab


@WorkflowFactory.register('ceda')
class CedaWorkflow(BaseWorkflow):
    """? or importer class see. cmip5"""


    def create_vocab(self, config):
        graph = Graph()
        graph.bind('skos', SKOS)
        # read vocabs from cache
        for file in glob("cache/*.xml"):
            graph.parse(file)
        
        namespace = Namespace("http://test.org/ceda/")

        for concept_scheme in config["concept_schemes"]:
            concept_scheme_uri = namespace[concept_scheme["name"]]
            graph.add((concept_scheme_uri, RDF.type, SKOS.ConceptScheme))
            graph.add((concept_scheme_uri, SKOS.prefLabel, Literal(concept_scheme["prefLabel"], lang='en')))
            if "definition" in concept_scheme.keys():
                        graph.add((concept_scheme_uri, SKOS.definition, Literal(concept_scheme["definition"], lang='en')))

            for sub_scheme in concept_scheme["sub_schemes"]:
                sub_namespace =  Namespace(sub_scheme["namespace"])
                graph.add((concept_scheme_uri, SKOS.narrower, sub_namespace[sub_scheme["name"]]))
                graph.add((sub_namespace[sub_scheme["name"]], SKOS.broader, concept_scheme_uri))
        
        return graph

    def run(self, config):
        vocab = self.create_vocab(config)

        return vocab
