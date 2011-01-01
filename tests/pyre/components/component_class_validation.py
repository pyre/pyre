#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
            number = pyre.properties.int(default=0)
            number.validators = pyre.constraints.isGreater(value=0)

    # access the exception that will get raised
    from pyre.constraints.exceptions import ConstraintViolationError
    # check the default values
    try:
        declare()
        assert False
    except ConstraintViolationError:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
