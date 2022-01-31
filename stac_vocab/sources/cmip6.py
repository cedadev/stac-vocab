# encoding: utf-8
"""
Maybe the workflows are so bespoke that they can't share a common importer
and the importers package becomes useful utils for common tasks...
"""
__author__ = 'Richard Smith'
__date__ = '17 Nov 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# from .base import BaseWorkflow
# from ..core import WorkflowFactory

# import json
# from rdflib import Graph, RDF, Namespace, SKOS

# # Use the JSON importer
# # Create and RDF object
# # return

# @WorkflowFactory.register('cmip6')
# class Cmip6Workflow(BaseWorkflow):
#     """? or importer class see. cmip5"""


#     def create_vocab(self, config):
#         graph = Graph()
#         graph.bind('skos', SKOS)
#         namespace = Namespace("http://test.org/cmip6/")
#         for concept in config["concepts"]:
#             with open(concept["location"]) as f:
#                 facets = json.load(f)
#                 graph.add((namespace[concept["name"]], RDF.type, SKOS.ConceptScheme))

#             for f, value in facets[concept["name"]].items():
#                 graph.add((namespace[f], RDF.type, SKOS.Concept))
#                 graph.add((namespace[f], SKOS.inScheme, namespace[concept["name"]]))
            
#         return graph

#     def run(self, config):
#         vocab = self.create_vocab(config)

#         return vocab


