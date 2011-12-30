#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that interface family names are recorded correctly
"""


def test():
    import pyre

    class interface(pyre.interface, family="test.interfaces.trivial"):
        """a trivial interface"""

    # check the family
    assert interface.pyre_family == ["test", "interfaces", "trivial"]
    # check the package name
    assert interface.pyre_getPackageName() == "test"

    return interface


# main
if __name__ == "__main__":
    test()


# end of file 
