#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise "isAll"
"""


def test():
    import pyre.constraints
    less = pyre.constraints.isLess(value=1)
    greater = pyre.constraints.isGreater(value=0)
    constraint = pyre.constraints.isAll(less, greater)

    constraint.validate(0.1)
    constraint.validate(0.5)
    constraint.validate(0.9)

    stranger = 1
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint in [less, greater]
        assert error.value == stranger

    stranger = 0
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint in [less, greater]
        assert error.value == stranger

    return constraint


# main
if __name__ == "__main__":
    test()


# end of file 
