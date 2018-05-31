=====
Usage
=====

To use Socials in a project::

    import socials


Let's assume that you have a list of href attribute values:

.. code-block:: python

    >>> hrefs = ['https://facebook.com/peterparker', 'https://techcrunch.com', 'https://github.com/lorey']

You can then extract all matches, i.e. social accounts and email addresses, as follows:

.. code-block:: python

    >>> socials.extract(hrefs).get_matches_per_platform()
    {'github': ['https://github.com/lorey'], 'facebook': ['https://facebook.com/peterparker']}

Or to extract matches for one specific platform only, e.g. github, you do:

.. code-block:: python

    >>> socials.extract(hrefs).get_matches_for_platform('github')
    ['https://github.com/lorey']
