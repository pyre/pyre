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

    # instantiate the component
    c1 = component(name="c1")
    # verify that the instance was recorded in the extent
    assert set(registrar.components[component]) == {c1}

    # instantiate another component
    c2 = component(name="c2")
    # verify that the instance was recorded in the extent
    assert set(registrar.components[component]) == {c1, c2}

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
