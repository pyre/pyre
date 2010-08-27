#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the trait defaults get bound correctly
"""


def test():
    import pyre

    # tuck this in a function so we can generate the exception at will
    def declare():
        # declare a component
        class base(pyre.component):
            """the base component"""
            number = pyre.properties.int()
            number.default = 0
            number.validators = pyre.constraints.isGreater(value=0)

    # check the default values
    try:
        declare()
        assert False
    except pyre.PyreError:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
