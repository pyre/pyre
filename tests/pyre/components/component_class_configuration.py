#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
    # declare the components
    component = declare()

    # print out the configuration 
    # import pyre
    # pyre.executive.configurator.dump()
    # print("component.p1 = {.p1!r}".format(component))
    # print("component.p2 = {.p2!r}".format(component))

    # check that the settings were read properly
    assert component.p1 == "sample - p1"
    assert component.p2 == "sample - p2"
    # and return the component
    return component
    

# main
if __name__ == "__main__":
    test()


# end of file 
