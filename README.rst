===========================
Dumbed Down Matching Engine
===========================

Implements a simple order matching engine. The server is implemented using
``tornado``.

------------
Installation
------------

Clone the ``git`` repository::

    $ git clone git@github.com:eigenholser/ddme.git

You will need ``curl`` and ``json_reformat``. On Ubuntu do this::

    $ sudo apt-get install curl
    $ sudo apt-get install yajl-tools

Create a Python virtual environment. Install Python dependencies::

    $ cd ddme
    $ mkvirtualenv ddme
    $ pip install -r requirements.txt

That's all there is to it. Now run it::

    $ python api.py

Or, if you want to run it on a different port::

    $ python api.py --port=4321

The validation tests are in the file ``test.sh``. The ``curl`` commands default
to port 3000. To validate, just invoke it on the command line::

    $ ./test.sh

Or if you've run the server on a different port::

    $ ./test.sh 4321

Notes
-----

* Implemented ``Book`` object using Singleton pattern. It seemed to fit this
  implementation. A scalable approach would certainly employ a different
  strategy.
* Return JSON response with fills. This was not specified in the spec but was
  helpful in development and, I would think, relevant information.
