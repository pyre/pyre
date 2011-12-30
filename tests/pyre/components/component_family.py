#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that component family names are recorded correctly
"""


def test():
    import pyre

    class component(pyre.component, family="test.components.trivial"):
        """a trivial component"""

    # check the family
    assert component.pyre_family == ["test", "components", "trivial"]
    # check the package name
    assert component.pyre_getPackageName() == "test"

    return component


# main
if __name__ == "__main__":
    test()


# end of file 
