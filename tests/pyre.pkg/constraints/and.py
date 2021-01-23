#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise combining two constraints using the operator "&"
    """

    # get the package
    import pyre.constraints
    # build a constraint
    less = pyre.constraints.isLess(value=1)
    greater = pyre.constraints.isGreater(value=0)
    constraint = greater & less
    # exercise it
    constraint.validate(0.1)
    constraint.validate(0.5)
    constraint.validate(0.9)

    # here is a case that fails
    stranger = 1
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint in [less, greater]
        assert error.value == stranger

    # another case that fails
    stranger = 0
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint in [less, greater]
        assert error.value == stranger

    # all done
    return constraint


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
