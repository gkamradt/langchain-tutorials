.. image:: https://github.com/seatgeek/thefuzz/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/seatgeek/thefuzz

TheFuzz
=======

Fuzzy string matching like a boss. It uses `Levenshtein Distance <https://en.wikipedia.org/wiki/Levenshtein_distance>`_ to calculate the differences between sequences in a simple-to-use package.

Requirements
============

-  Python 3.7 or higher
-  difflib
-  `python-Levenshtein <https://github.com/ztane/python-Levenshtein/>`_ (optional, provides a 4-10x speedup in String
   Matching, though may result in `differing results for certain cases <https://github.com/seatgeek/fuzzywuzzy/issues/128>`_)

For testing
~~~~~~~~~~~
-  pycodestyle
-  hypothesis
-  pytest

Installation
============

Using PIP via PyPI

.. code:: bash

    pip install thefuzz

or the following to install `python-Levenshtein` too

.. code:: bash

    pip install thefuzz[speedup]


Using PIP via Github

.. code:: bash

    pip install git+git://github.com/seatgeek/thefuzz.git@0.19.0#egg=thefuzz

Adding to your ``requirements.txt`` file (run ``pip install -r requirements.txt`` afterwards)

.. code:: bash

    git+ssh://git@github.com/seatgeek/thefuzz.git@0.19.0#egg=thefuzz

Manually via GIT

.. code:: bash

    git clone git://github.com/seatgeek/thefuzz.git thefuzz
    cd thefuzz
    python setup.py install


Usage
=====

.. code:: python

    >>> from thefuzz import fuzz
    >>> from thefuzz import process

Simple Ratio
~~~~~~~~~~~~

.. code:: python

    >>> fuzz.ratio("this is a test", "this is a test!")
        97

Partial Ratio
~~~~~~~~~~~~~

.. code:: python

    >>> fuzz.partial_ratio("this is a test", "this is a test!")
        100

Token Sort Ratio
~~~~~~~~~~~~~~~~

.. code:: python

    >>> fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
        91
    >>> fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
        100

Token Set Ratio
~~~~~~~~~~~~~~~

.. code:: python

    >>> fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
        84
    >>> fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
        100

Partial Token Sort Ratio
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> fuzz.token_sort_ratio("fuzzy was a bear", "wuzzy fuzzy was a bear")
        84
    >>> fuzz.partial_token_sort_ratio("fuzzy was a bear", "wuzzy fuzzy was a bear")
        100
        
Process
~~~~~~~

.. code:: python

    >>> choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
    >>> process.extract("new york jets", choices, limit=2)
        [('New York Jets', 100), ('New York Giants', 78)]
    >>> process.extractOne("cowboys", choices)
        ("Dallas Cowboys", 90)

You can also pass additional parameters to ``extractOne`` method to make it use a specific scorer. A typical use case is to match file paths:

.. code:: python

    >>> process.extractOne("System of a down - Hypnotize - Heroin", songs)
        ('/music/library/good/System of a Down/2005 - Hypnotize/01 - Attack.mp3', 86)
    >>> process.extractOne("System of a down - Hypnotize - Heroin", songs, scorer=fuzz.token_sort_ratio)
        ("/music/library/good/System of a Down/2005 - Hypnotize/10 - She's Like Heroin.mp3", 61)

.. |Build Status| image:: https://github.com/seatgeek/thefuzz/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/seatgeek/thefuzz
