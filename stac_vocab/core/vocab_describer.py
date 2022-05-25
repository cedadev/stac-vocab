# encoding: utf-8
"""
Vocab Description
================
"""
__author__ = "Rhys Evans"
__date__ = "1 May 2022"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "rhys.r.evans@stfc.ac.uk"


import logging

# Python imports
from pathlib import Path
from typing import Optional

import yaml

# 3rd Party Imports
from pydantic import BaseModel


LOGGER = logging.getLogger(__name__)


class VocabDescription(BaseModel):
    """Top level container for VocabDescription."""

    namespace: str

    workflow: str
    workflow_inputs: dict

    def __repr__(self):
        return yaml.dump(self.dict())


class VocabDescriptions:
    """
    Holds references to all the description files and handles loading
    and returning a :py:obj:`VocabDescription`
    """

    def __init__(self, root_path: Optional[str] = None):
        """
        :param root_path: Path to the root of the yaml store
        """

        self.external_vocab_descriptions = {}
        self.general_vocab_description = {}

        self._load_external_vocab_descriptions(f"{root_path}/external_vocabs")
        self._load_general_vocab(root_path)

    def _load_external_vocab_descriptions(self, path: str) -> None:
        """
        Loads the yaml files for the external vocabularies.

        :param path: Path to the external vocabularies descriptions directory
        """

        files = load_description_files(path)

        if not files:
            LOGGER.error(
                "No description files found. "
                "Check the path in your configuration. Exiting..."
            )
            exit()

        for file in files:
            with open(file) as reader:
                data = yaml.safe_load(reader)
                vocab_description = VocabDescription(**data)
                self.external_vocab_descriptions[vocab_description.namespace] = vocab_description

    def _load_general_vocab(self, path: str) -> None:
        """
        Loads the yaml file for the general vocabulary.

        :param path: Path to the general vocabulary description directory
        """

        file = load_description_files(path)[0]

        if not file:
            LOGGER.error(
                "No general description file found. "
                "Check the path in your configuration. Exiting..."
            )
            exit()

        with open(file) as reader:
            data = yaml.safe_load(reader)
            self.general_vocab_description = VocabDescription(**data)

    def get_external_vocab_descriptions(self) -> list[VocabDescription]:
        """
        Get all the external vocabulary descriptions.
        """

        return self.external_vocab_descriptions.values()
    
    def get_general_vocab_description(self) -> VocabDescription:
        """
        Get all the external vocabulary descriptions.
        """

        return self.general_vocab_description
    
    def get_description(self, namespace: str) -> VocabDescription:
        """
        Get the description for the given namespace.

        :param namespace: namespace for which to retrieve the description
        """

        if namespace == "ceda":
            return self.general
        else:
            return self.external_vocab_descriptions[namespace]


def load_description_files(path: str) -> list[str]:
    """
    Load the yaml description files under the given path

    :param path: Path for the description files
    """

    exts = [".yml", ".yaml"]
    return [p for p in Path(path).glob("*") if p.suffix in exts]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root", help="root from which to load all the yaml description files"
    )
    parser.add_argument("namespace", help="namespace to retrieve description for")

    args = parser.parse_args()

    descriptions = VocabDescriptions(args.root)

    description = descriptions.get_description(args.namespace)

    print(description)
