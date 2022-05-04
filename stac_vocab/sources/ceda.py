# encoding: utf-8
"""
Top level vocab
"""
__author__ = 'Richard Smith'
__date__ = '17 Nov 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from pydantic import BaseModel

from ..core import WorkflowFactory, BaseWorkflow, CEDAConceptScheme, CEDASubScheme


class CEDAWorkflowInputs(BaseModel):
    """Common model for concept scheme."""

    concept_schemes: list[CEDAConceptScheme]


@WorkflowFactory.register('ceda')
class CedaWorkflow(BaseWorkflow):
    """? or importer class see. cmip5"""
    ...
    INPUTS_CLASS = CEDAWorkflowInputs

    def run(self):

        self.create_vocab(self.inputs.concept_schemes)

    def parser(self, raw_concept_scheme):
        ...