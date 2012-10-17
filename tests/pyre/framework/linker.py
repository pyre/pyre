#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify the linker is accessible through the executive
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()

    # access the linker
    assert executive.linker is not None

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
