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

import json
import os

from typing import Optional
from pydantic import BaseModel

from ..core import WorkflowFactory, BaseWorkflow, CEDAConcept, CEDAConceptScheme


class Cmip6Concept(BaseModel):
    """Common model for concept scheme."""

    label: str

    alt_label: Optional[str]
    label_extended: Optional[str]


class Cmip6ConceptScheme(BaseModel):
    """Common model for concept scheme."""

    name: str

    pref_label: str
    alt_label: Optional[str]
    description: str

    location: str


class Cmip6WorkflowInputs(BaseModel):
    """Common model for concept scheme."""

    concept_schemes: list[Cmip6ConceptScheme]


@WorkflowFactory.register('cmip6')
class Cmip6Workflow(BaseWorkflow):
    """? or importer class see. cmip5"""
    INPUTS_CLASS = Cmip6WorkflowInputs

    def run(self):

        concept_schemes = []

        for concept_scheme in self.inputs.concept_schemes:
            concept_schemes.append(self.parser(concept_scheme))
        
        self.create_vocab(concept_schemes)
    
    def parser(self, raw_concept_scheme):

        concept_scheme = CEDAConceptScheme(
            name = raw_concept_scheme.name,
            pref_label = raw_concept_scheme.pref_label
        )

        if raw_concept_scheme.alt_label:

            concept_scheme.alt_label = raw_concept_scheme.alt_label

        if raw_concept_scheme.description:

            concept_scheme.definition = raw_concept_scheme.description

        with open(raw_concept_scheme.location) as f:

            facets = json.load(f)
            concepts = []

            if isinstance(facets[raw_concept_scheme.name], dict):

                for name, raw_concept in facets[raw_concept_scheme.name].items():
        
                    if isinstance(raw_concept, str):

                        concepts.append(
                            CEDAConcept(
                                name = name,
                                pref_label = name,
                                definition = raw_concept
                            )
                        )

                    else:

                        try:

                            raw_concept = Cmip6Concept(**raw_concept)
                        
                        except:

                            raw_concept = Cmip6Concept(
                                label = raw_concept["experiment_id"],
                                alt_label = raw_concept["experiment"],
                                label_extended = raw_concept["description"]
                            )

                        if raw_concept.label:
                            pref_label = raw_concept.label
                        else:
                            pref_label = name

                        concept = CEDAConcept(
                            name = name,
                            pref_label = pref_label
                        )

                        if raw_concept.label_extended:
                            concept.definition = raw_concept.label_extended

                        if raw_concept.alt_label:
                            concept.alt_label = raw_concept.alt_label
                        
                        concepts.append(concept)
            
            else:

                for name in facets[raw_concept_scheme.name]:
        
                    concepts.append(
                        CEDAConcept(
                            name = name.replace(' ', '_'),
                            pref_label = name
                        )
                    )

        concept_scheme.concepts = concepts

        return concept_scheme


