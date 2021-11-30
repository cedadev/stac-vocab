# encoding: utf-8
"""
Can we use importer classes for shared workflows
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


# @WorkflowFactory.register('Cmip6Workflow')
class Cmip6Workflow(BaseWorkflow):

    IMPORTER_CLASS = JSONImporter

    def run(self, config):

        importer = self.IMPORTER_CLASS(config)

        vocab = importer.create_vocab()

        return vocab



