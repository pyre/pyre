#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the Actor metaclass decorates class records properly
"""


def test():
    # access
    from pyre.components.Component import Component
    from pyre.components.Inventory import Inventory

    # declare a class
    class base(Component):
        """test class"""

    # did my ancestor list get built properly
    assert base._pyre_configurables == (base, Component)
    # did the _pyre_Inventory embedded class get built?
    inventory = base._pyre_Inventory
    # is it properly subclassed?
    assert issubclass(inventory, Inventory)
        
    return base


# main
if __name__ == "__main__":
    test()


# end of file 
