#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a name with capitals is quoted, so that it keeps them
"""


def test():
    """
    Render a name with a capital, and check it is quoted
    """
    # access the package
    import pyre.db

    # make a mill
    mill = pyre.db.backends.standard.mill(name="identifiers")
    # render the name
    text = mill.identifier("Weather")
    # and check it
    assert text == '"Weather"', text
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
