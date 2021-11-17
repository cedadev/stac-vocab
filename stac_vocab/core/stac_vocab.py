"""Main module."""

__author__ = """richard smith"""
__contact__ = 'richard.d.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


class VocabImporter:
    """Top level workflow class"""
    ...

    def process(self):
        ...
        # collect workflows (some might be skipped)

        # Output number of workflows to run/skipped
        # run workflows
        for workflow in workflows:
            vocab = workflow.run()

            # output vocab to file


        # Link ceda vocab to other vocabs
