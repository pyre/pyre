#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the trait defaults get validated properly
"""


def test():
    import pyre

    # tuck this in a function so we can generate the exception at will
    def simple():
        # declare a component
        class base(pyre.component):
            """the base component"""
            number = pyre.properties.int(default=0)
            number.validators = pyre.constraints.isGreater(value=0)

    # and another that assigns the validators in an iterable
    def iterable():
        class base(pyre.component):
            """the base component"""
            number = pyre.properties.int(default=0)
            number.validators = (pyre.constraints.isGreater(value=0),)

    # check the simple case
    try:
        simple()
        assert False
    except pyre.component.ConstraintViolationError:
        pass

    # check the iterable case
    try:
        iterable()
        assert False
    except pyre.component.ConstraintViolationError:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
