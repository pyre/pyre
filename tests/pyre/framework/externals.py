#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


"""
Sanity check: verify that the package manager is accessible
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()

    # access the external package manager
    assert executive.externals is not None

    # all done
    return executive


# main
if __name__ == "__main__":
    # do...
    test()


# end of file 
