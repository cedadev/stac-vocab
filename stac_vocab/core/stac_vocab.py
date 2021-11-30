"""Main module."""

__author__ = """richard smith"""
__contact__ = 'richard.d.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

from .register import WorkflowFactory

cache_config = {
    "workflows": {
        "cmip6": {
            "concepts": [
                {
                    "name": "source_id",
                    "location": "../../CMIP6_source_id.json",
                },
                {
                    "name": "source_type",
                    "location": "../../CMIP6_source_type.json",
                },
            ],
        },
    }
}

ceda_config = {
    "concept_schemes": [
        {
            "name": "model",
            "description": "A model is a ...",
            "sub_schemes": [
                {
                    "name": "source_id",
                    "namespace": "http://test.org/cmip6/",
                },
                {
                    "name": "model",
                    "namespace": "http://test.org/cmip5/",
                }
            ],
        },
    ]
}

class VocabImporter:
    """Top level workflow class"""
    ...

    def create_cache(self):
        ...
        # collect workflows (some might be skipped)

        # Output number of workflows to run/skipped
        # run workflows
        print(WorkflowFactory.registry.items())
        for workflow_name, workflow in WorkflowFactory.registry.items():
            if workflow_name in cache_config["workflows"].keys():
                vocab = workflow().run(cache_config["workflows"][workflow_name])
                # output vocab to file
                vocab.serialize(destination=f"cache/{workflow_name}.xml", format='xml')

    def create_ceda(self):
        ...

        # run ceda workflow
        workflow = WorkflowFactory.registry["ceda"]
        vocab = workflow().run(ceda_config)
        
        # output vocab to file
        vocab.serialize(destination=f"cache/ceda.xml", format='xml')
