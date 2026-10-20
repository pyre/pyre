#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise "isPositive"
"""


def test():
    import pyre.constraints

    # make the constraint
    constrain = pyre.constraints.isPositive()

    # values greater than zero are accepted
    constrain(1)
    constrain(1.1)
    constrain(2)

    # zero and anything below it
    for stranger in (0, -1):
        # must be
        try:
            # refused
            constrain(stranger)
            # so getting here is a bug
            assert False, f"{stranger} was accepted as positive"
        # by the constraint
        except constrain.ConstraintViolationError as error:
            # that knows who it is
            assert error.constraint == constrain
            # and what it refused
            assert error.value == stranger

    # all done
    return constrain


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
