#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a quote inside a name is doubled
"""


def test():
    """
    Render a name with a double quote in it, and check the quote is doubled
    """
    # access the package
    import pyre.db

    # make a mill
    mill = pyre.db.backends.standard.mill(name="identifiers")
    # render the name
    text = mill.identifier('a"b')
    # and check it
    assert text == '"a""b"', text
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
