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
from rdflib import Graph, RDF, Namespace, SKOS

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
        for concept in config["concepts"]:
            with open(concept["location"]) as f:
                facets = json.load(f)
                graph.add((namespace[concept["name"]], RDF.type, SKOS.ConceptScheme))

            for f, value in facets[concept["name"]].items():
                graph.add((namespace[f], RDF.type, SKOS.Concept))
                graph.add((namespace[f], SKOS.inScheme, namespace[concept["name"]]))
            
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
            graph.add((namespace[concept_scheme["name"]], RDF.type, SKOS.ConceptScheme))

            for sub_scheme in concept_scheme["sub_schemes"]:
                sub_namespace =  Namespace(sub_scheme["namespace"])
                graph.add((sub_namespace[sub_scheme["name"]], SKOS.narrower, namespace[concept_scheme["name"]]))
        
        return graph

    def run(self, config):
        vocab = self.create_vocab(config)

        return vocab
