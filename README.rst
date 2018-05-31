=======
Socials
=======


.. image:: https://img.shields.io/pypi/v/socials.svg
        :target: https://pypi.python.org/pypi/socials

.. image:: https://img.shields.io/travis/lorey/socials.svg
        :target: https://travis-ci.org/lorey/socials

.. image:: https://readthedocs.org/projects/socials/badge/?version=latest
        :target: https://socials.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Social Account Detection and Extraction for Python


* Free software: GNU General Public License v3
* Documentation: https://socials.readthedocs.io.
* Source: https://github.com/lorey/socials


Features
--------

* Detect and extract URLs of social accounts: throw in URLs, get back URLs of social media profiles by type.
* Currently supports Facebook, Twitter, LinkedIn, GitHub, and Emails.

Usage
-----

Install it with ``pip install socials`` and use it as follows:

.. code-block:: python

    >>> urls = ['https://facebook.com/peterparker', 'https://techcrunch.com', 'https://github.com/lorey']
    >>> socials.extract().get_matches_per_platform()
    {'github': ['https://github.com/lorey'], 'facebook': ['https://facebook.com/peterparker']}

Development
-----------

Create virtual envirenment ``venv`` with ``virtualenv -p /usr/bin/python3 venv``.
Activate the environment with ``source venv/bin/activate``.
Install the development requirements with ``pip install -r requirements-dev.txt``.
Run the tests: ``tox`` or ``python setup.py test``

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
