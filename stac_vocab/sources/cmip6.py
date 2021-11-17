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

from .base import BaseWorkflow
from stac_vocab import WorkflowFactory

# Use the JSON importer
# Create and RDF object
# return

config = {

}


@WorkflowFactory.register('Cmip6Workflow')
class Cmip6Workflow(BaseWorkflow):
    """? or importer class see. cmip5"""


    def create_vocab(self):
        ...

    def run(self, config):



        vocab = self.create_vocab

        return vocab



