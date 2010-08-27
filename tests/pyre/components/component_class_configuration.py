#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
A more elaborate component declaration
"""


def declare():
    import pyre

    class component(pyre.component, family="sample.configuration"):
        """a test component"""
        # properties
        p1 = pyre.properties.str(default="p1")
        p2 = pyre.properties.str(default="p2")

        # behaviors
        @pyre.components.export
        def do(self):
            """behave"""
      
    return component


def test():
    component = declare()
    # check that the setting were read properly
    assert component.p1 == "sample - p1"
    assert component.p2 == "sample - p2"
    # and return the component
    return component
    

# main
if __name__ == "__main__":
    test()


# end of file 
