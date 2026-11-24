#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a name of lower case letters, digits and underscores is written as it is
"""


def test():
    """
    Render an ordinary name, and check it is left alone
    """
    # access the package
    import pyre.db

    # make a mill
    mill = pyre.db.backends.standard.mill(name="identifiers")
    # render the name
    text = mill.identifier("granules_2026")
    # and check it
    assert text == "granules_2026", text
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
