To install dependencies:

    make install

If you would like to add additional dependencies, simply add them to
`requirements.txt` and run `make install` again.

To run the test suite:

    make test

To run the app:

    ./run.py

(All of these are also available in the "Project" menu)

This is set up to use Python 3 by default. If you would prefer to use Python 2,
update the first line of `run.py` to be:

    #! /usr/bin/env python2

and `python` in `makefile`:

    python = python2

Then run `make install` as usual.