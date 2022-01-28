==========
STAC Vocab
==========

Retrieve controlled vocabularies from external sources to generate a local cache in a common format.

Construct a shared vocabulary which can map to one or more sub-vocabs.

.. image:: docs/images/vocab_generator.png

Getting Started
---------------

.. code-block:: bash

    python -m venv venv
    pip install -r requirements.txt

Running
-------

.. code-block:: bash

    stac_vocab -h
    usage: stac_vocab [-h] conf

    Generates the CEDA STAC vocabulary, pulling in remote sources and linking vocabularies to the canonical CEDA facets

    positional arguments:
    conf        Path to configuration file

    optional arguments:
    -h, --help  show this help message and exit


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `cedadev/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
