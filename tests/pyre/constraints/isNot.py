#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise "isNot"
"""


def test():
    import pyre.constraints
    less = pyre.constraints.isLess(value=0)
    constraint = pyre.constraints.isNot(less)

    constraint.validate(0)
    constraint.validate(1.0)

    stranger = -1
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint == constraint
        assert error.value == stranger

    return constraint


# main
if __name__ == "__main__":
    test()


# end of file 
