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

    # declare a component
    class base(pyre.component, family="sample.base"):
        """a base component"""
        common = pyre.properties.str(default="base")

    # derive another one from it
    class intermediate(base):
        """an intermediate component in the hierarchy that doesn't declare a family"""
        middle = pyre.properties.str(default="intermediate")

    # and a final one
    class derived(intermediate, family="sample.derived"):
        """a derived component"""
        extra = pyre.properties.str(default="derived")

    return base, intermediate, derived


def test():
    # get the declarations
    base, intermediate, derived = declare()
    # instantiate
    d = derived(name="d")
    # check that the settings were read properly
    assert d.common == "d - common"
    assert d.middle == "d - middle"
    assert d.extra == "d - extra"
    # and return the component classes
    return d
    

# main
if __name__ == "__main__":
    test()


# end of file 
