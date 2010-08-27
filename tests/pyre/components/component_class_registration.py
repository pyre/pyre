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
    import pyre

    # declare an interface
    class interface(pyre.interface):
        """an interface"""
        # properties
        p1 = pyre.property()
        p2 = pyre.property()
        # behavior
        @pyre.provides
        def do(self):
            """behave"""
        
    # declare a component
    class component(pyre.component, family="test", implements=interface):
        """a component"""
        # traits
        p1 = pyre.property()
        p1.default = "p1"

        p2 = pyre.property()
        p2.default = "p2"

        @pyre.export
        def do(self):
            """behave"""
            return "component"

    # fetch the registrar
    import pyre
    registrar = pyre.executive.registrar

    # check that the interface is corectly registered
    assert registrar.interfaces == {interface}
    # check that the component is correctly registered
    assert set(registrar.components.keys()) == {component}
    # check that the set of interface implementors is correct
    assert registrar.implementors[interface] == {component}

    return component
     

# main
if __name__ == "__main__":
    test()
    # now check that the components were destroyed when they went out of scope
    import pyre
    registrar = pyre.executive.registrar
    for cls, extent in registrar.components.items():
        assert set(extent) == set()


# end of file 
