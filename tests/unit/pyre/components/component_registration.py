#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise component registration
"""


def test():
    # access
    import pyre.components
    from pyre.components.Component import Component
    from pyre.components.Interface import Interface
    from pyre.components.Property import Property

    # declare an interface
    class interface(Interface):
        """an interface"""
        # properties
        p1 = Property()
        p2 = Property()
        # behavior
        @pyre.components.provides
        def do(self):
            """behave"""
        
    # declare a component
    class component(Component, family="test", implements=interface):
        """a component"""
        # traits
        p1 = Property()
        p1.default = "p1"

        p2 = Property()
        p2.default = "p2"

        @pyre.components.export
        def do(self):
            """behave"""
            return "component"

    # fetch the registrar
    import pyre
    registrar = pyre.executive().registrar

    # check that the interface is corectly registered
    assert registrar.interfaces == {interface}
    # check that the component is correctly registered
    assert set(registrar.components.keys()) == {component}
    # check that the set of interface implementors is correct
    assert registrar.implementors[interface] == {component}

    # instantiate the component
    c = component(name="c")
    # verify that the instance was recorded in the extent
    assert set(registrar.components[component]) == {c}

    return component
     

# main
if __name__ == "__main__":
    test()


# end of file 
