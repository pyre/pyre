#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercises the component registrar
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()

    # access the component registrar
    reg = executive.registrar
    assert reg is not None

    # get to the singleton directly
    from pyre.components.Registrar import Registrar
    rd = Registrar()
    # verify that these two are the same object
    assert reg is rd

    # get to the singleton through the factory
    rf = pyre.framework.newComponentRegistrar()
    # verify that this also the same object
    assert reg is rf

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
