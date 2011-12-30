#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Check explicit and implicit interface compatibility
"""


def test():
    import pyre

    # declare an interface
    class interface(pyre.interface):
        """a simple interface"""
        # properties
        name = pyre.property()
        name.default = "my name"

        @pyre.provides
        def say(self):
            """say my name"""

    # declare a component that claims to implement this interface explicitly
    class explicit(pyre.component, family="tests.explicit", implements=interface):
        """a simple component"""
        # properties
        name = pyre.property()
        name.default = "whatever"

        @pyre.export
        def say(self):
            """say my name"""
            return self.name

    # declare a component that implements this interface implicitly
    class implicit(pyre.component, family="tests.implicit"):
        """a simple component"""
        # properties
        name = pyre.property()
        name.default = "whatever"

        @pyre.export
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
