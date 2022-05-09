"""Console script for stac_vocab."""

__author__ = """richard smith"""
__contact__ = 'richard.d.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
import argparse
import sys

from stac_vocab.core.stac_vocab import VocabImporter

def main():
    """Console script for stac_vocab."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "conf_path", help="path to config file"
    )
    args = parser.parse_args()

    vocab_importer = VocabImporter(args.conf_path)
    vocab_importer.create_cache()
    vocab_importer.create_ceda_vocab()

    print("Code run successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
