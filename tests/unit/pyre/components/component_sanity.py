#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: declare a trivial component
"""


def test():
    from pyre.components.Component import Component
    from pyre.components.Inventory import Inventory

    class component(Component, family="trivial"):
        """a trivial component"""
     
    # check the basics
    assert component._pyre_name == "component"
    assert component._pyre_family == "trivial"
    assert component._pyre_configurables == (component, Component)
    assert component._pyre_implements == None
    # check the embedded inventory class
    assert issubclass(component._pyre_Inventory, Inventory)

    return component


# main
if __name__ == "__main__":
    test()


# end of file 
