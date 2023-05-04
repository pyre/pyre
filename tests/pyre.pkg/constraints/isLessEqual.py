#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Exercise "isLessEqual"
"""


def test():
    import pyre.constraints
    constraint = pyre.constraints.isLessEqual(value=1)

    constraint.validate(1.)
    constraint.validate(0.9)
    constraint.validate(0)

    stranger = 1.5
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint == constraint
        assert error.value == stranger

    return constraint


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
