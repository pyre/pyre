#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise "isLike"
    """

    # get the package
    import pyre.constraints

    # build a constraint
    phone = r"(\+\d+\s+)?\(?\d{3}\)?(.|\s+)\d{3}[-.]\d{4}"
    constraint = pyre.constraints.isLike(regexp=phone)

    # exercise with good values
    constraint.validate("(877) 877-0987")
    constraint.validate("(877) 877.0987")
    constraint.validate("877.877.0987")
    constraint.validate("+1 877.877.0987")

    # a case that should fail
    stranger = "(877) 877-097"
    # try to
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
