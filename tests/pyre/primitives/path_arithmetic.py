#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


"""
Exercise the path primitive
"""


def test():
    # the home of the factory
    import pyre.primitives
    # start with
    root = pyre.primitives.path('/')
    # my development area
    home = 'Users/mga/dv'
    # the location of this test
    here = pyre.primitives.path('pyre-1.0/tests/pyre/primitives/path_arithmetic.py')

    # assemble
    total = root / home / here
    # check
    assert str(total) == '/Users/mga/dv/pyre-1.0/tests/pyre/primitives/path_arithmetic.py'

    # let's try another
    total = '/' / pyre.primitives.path(home) / str(here)
    # check
    assert str(total) == '/Users/mga/dv/pyre-1.0/tests/pyre/primitives/path_arithmetic.py'

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
