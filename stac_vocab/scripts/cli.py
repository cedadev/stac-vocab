"""Console script for stac_vocab."""

__author__ = """richard smith"""
__contact__ = 'richard.d.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
import argparse
import sys
from stac_vocab.core.stac_vocab import VocabImporter
# list_workflows
# Run all
# Run specific workflows


def main():
    """Console script for stac_vocab."""
    parser = argparse.ArgumentParser(
        description="""
            Generates the CEDA STAC vocabulary, pulling in remote sources and linking vocabularies to the canonical CEDA facets
        """
        )
    #parser.add_argument('_', nargs='*') # what is this for?
    parser.add_argument('conf', help="Path to configuration file")
    args = parser.parse_args()

    vocab_importer = VocabImporter(config_file=args.conf)
    vocab_importer.create_cache()
    vocab_importer.create_ceda_concept_scheme()

    print("Code run successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
