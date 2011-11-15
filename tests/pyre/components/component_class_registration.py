#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise component registration
"""

# access the framework
import pyre


def test():
    # declare an interface
    class interface(pyre.interface):
        """an interface"""
        # properties
        p1 = pyre.properties.str()
        p2 = pyre.properties.str()
        # behavior
        @pyre.provides
        def do(self):
            """behave"""
        
    # declare a component
    class component(pyre.component, family="test", implements=interface):
        """a component"""
        # traits
        p1 = pyre.properties.str(default="p1")
        p2 = pyre.properties.str(default="p2")

        @pyre.export
        def do(self):
            """behave"""
            return "component"

    # fetch the registrar
    registrar = pyre.executive.registrar

    # check that the interface is correctly registered
    assert interface in registrar.interfaces
    # check that the component is correctly registered
    assert component in registrar.components
    # check that the set of {interface} implementors is correct
    assert registrar.implementors[interface] == {component}

    # now examine the component inventory
    behaviors = tuple(map(component.pyre_getTraitDescriptor, ["do"]))
    properties = tuple(map(component.pyre_getTraitDescriptor, ["p1", "p2"]))
    # get the class inventory
    inventory = component.pyre_inventory
    # loop over behaviors and make sure they are not present in the inventory
    for trait in behaviors:
        # verify it's not there
        assert trait not in inventory
    # loop over the properties and verify they are represented in the inventory
    for trait in properties:
        # verify existence
        assert trait in inventory

    return component
     

# main
if __name__ == "__main__":
    # run the test
    component = test()
    # verify that all instances of {component} have been destroyed
    assert tuple(pyre.executive.registrar.components[component]) == ()


# end of file 
