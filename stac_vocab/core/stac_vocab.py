"""Main module."""

__author__ = """richard smith"""
__contact__ = 'richard.d.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
import configparser

from .register import WorkflowFactory
from .vocab_describer import VocabDescriptions
import stac_vocab.sources


class VocabImporter:
    """Top level workflow class"""
    ...

    def __init__(self, config_path: str = None):
        ...

        if not config_path:
            config_path = os.path.join(
                os.environ["HOME"], ".stac_vocab.cfg"
            )
        
        self.conf = configparser.ConfigParser()
        self.conf.read(config_path)

        vocab_descriptions = VocabDescriptions(self.conf["VOCAB"]["description_path"])
        self.vocab_descriptions = vocab_descriptions

    def create_cache(self):
        ...
        # collect workflows (some might be skipped)

        # Output number of workflows to run/skipped
        # run workflows

        for external_vocab_description in self.vocab_descriptions.get_external_vocab_descriptions():

            namespace = external_vocab_description.namespace
            inputs = external_vocab_description.workflow_inputs

            workflow = WorkflowFactory.registry.get(external_vocab_description.workflow)(self.conf, namespace, inputs)
            workflow.run()

    def create_ceda(self):
        ...
        # run ceda workflow
        general_vocab_description = self.vocab_descriptions.get_general_vocab_description()

        namespace = general_vocab_description.namespace
        inputs = general_vocab_description.workflow_inputs

        workflow = WorkflowFactory.registry.get(general_vocab_description.workflow)(self.conf, namespace, inputs)
        workflow.run()
