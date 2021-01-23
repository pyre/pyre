#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise "isLessEqual"
    """

    # get the package
    import pyre.constraints
    # build a constraint
    constraint = pyre.constraints.isLessEqual(value=1)

    # exercise with good values
    constraint.validate(1.)
    constraint.validate(0.9)
    constraint.validate(0)

    # a case that should fail
    stranger = 1.5
    # attempt to
    try:
        # validate it
        constraint.validate(stranger)
        # which should fail
        assert False, "unreachable"
    # catch the error
    except constraint.ConstraintViolationError as error:
        # verify the error conditions
        assert error.constraint == constraint
        assert error.value == stranger

    # all done
    return constraint


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
