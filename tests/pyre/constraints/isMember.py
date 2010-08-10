#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise "isMember"
"""


def test():
    import pyre.constraints
    constraint = pyre.constraints.isMember("one", "two", "three")

    constraint.validate("one")
    constraint.validate("two")
    constraint.validate("three")

    stranger = "zero"
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
