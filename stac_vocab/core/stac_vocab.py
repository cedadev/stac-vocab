"""Main module."""

__author__ = """richard smith"""
__contact__ = 'richard.d.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

from .register import WorkflowFactory
from .conf import Configuration


class VocabImporter:
    """Top level workflow class"""
    
    def __init__(self, config_file: str):
        self.config = Configuration.load_yaml(config_file)

    def create_cache(self):
        ...
        # collect workflows (some might be skipped)

        # Output number of workflows to run/skipped
        # run workflows
        print(WorkflowFactory.registry.items())
        for workflow_name, workflow in WorkflowFactory.registry.items():
            workflow_config = self.config.workflows.get(workflow_name)
            if workflow_config:
                vocab = workflow().run(workflow_config)
                # output vocab to file
                vocab.serialize(destination=f"cache/{workflow_name}.xml", format='xml')

    def create_ceda_concept_scheme(self) -> None:
        ...

        # run ceda workflow
        workflow = WorkflowFactory.registry["ceda"]
        vocab = workflow().run(self.config.concept_schemes)
        
        # output vocab to file
        vocab.serialize(destination=f"cache/ceda.xml", format='xml')
