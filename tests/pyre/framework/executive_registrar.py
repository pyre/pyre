#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercises the component registrar
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive(managers=pyre.framework)

    # access the component registrar
    reg = executive.registrar
    assert reg is not None

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
