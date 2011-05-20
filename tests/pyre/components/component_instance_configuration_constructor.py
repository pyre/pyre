#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that configuration settings are available in the component constructor
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


        # meta method
        def __init__(self, name, **kwds):
            super().__init__(name=name, **kwds)

            # check that configuration setting have been applied after super().__init__ returns
            # a specially named component...
            if name == 'c':
                # has a known configuration applied
                assert self.p1 == 'p1 - instance'
                assert self.p2 == 'p2 - instance'

      
    return component


def test():
    # get the declaration
    component = declare()
    # instantiate
    c = component(name="c")
    # check that the configuration setting were transferred correctly
    assert c.p1 == "p1 - instance"
    assert c.p2 == "p2 - instance"
    # and return the component instance
    return c
    

# main
if __name__ == "__main__":
    test()


# end of file 
