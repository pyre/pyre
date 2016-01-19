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
    # the location of this test
    here = pyre.primitives.path('/Users/mga/dv/pyre-1.0/tests/pyre/primitives/path_parts.py')

    # verify that the {path} property returns something identical to the str representation
    assert here.path == str(here)
    # check that we extract the parts correctly
    assert list(here.parts) == ['/'] + str(here).split('/')[1:]
    # check the name
    assert here.name == 'path_parts.py'
    # check the suffix
    assert here.suffix == '.py'
    # check the stem
    assert here.stem == 'path_parts'

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
