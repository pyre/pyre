#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Check explicit and implicit interface compatibility
"""


def test():
    import pyre.components
    from pyre.components.Component import Component
    from pyre.components.Interface import Interface
    from pyre.components.Property import Property

    # declare an interface
    class interface(Interface):
        """a simple interface"""
        # properties
        name = Property()
        name.default = "my name"

        @pyre.components.provides
        def say(self):
            """say my name"""

    # declare a component that claims to implement this interface explicitly
    class explicit(Component, family="tests", implements=interface):
        """a simple component"""
        # properties
        name = Property()
        name.default = "whatever"

        @pyre.components.export
        def say(self):
            """say my name"""
            return self.name

    # declare a component that implements this interface implicitly
    class implicit(Component, family="tests"):
        """a simple component"""
        # properties
        name = Property()
        name.default = "whatever"

        @pyre.components.export
        def say(self):
            """say my name"""
            return self.name

    # check interface compatibility
    assert explicit.pyre_isCompatible(interface)
    assert implicit.pyre_isCompatible(interface)

    return explicit, implicit, interface


# main
if __name__ == "__main__":
    test()


# end of file 
