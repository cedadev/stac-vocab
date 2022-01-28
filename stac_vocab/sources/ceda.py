# encoding: utf-8
"""
Top level vocab
"""
__author__ = 'Richard Smith'
__date__ = '17 Nov 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from .base import BaseWorkflow
from stac_vocab.core import WorkflowFactory

import json
from rdflib import Graph, RDF, Namespace, SKOS

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
