#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Check that a component's behaviors are callable
"""


def test():
    import pyre.components
    from pyre.components.Component import Component
    from pyre.components.Property import Property

    # declare a component
    class component(Component):
        """a test component"""
        # behavior
        @pyre.components.export
        def do(self):
            """behave"""
            return True

    # instantiate it
    c = component(name="test")
    # invoke its behavior
    assert c.do()
    # and return it
    return c


# main
if __name__ == "__main__":
    test()


# end of file 
