#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Exercises the component registrar
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()

    # access the component registrar
    assert executive.registrar is not None

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
