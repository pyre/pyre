#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


"""
Verify that trait assignments that violate constraints are flagged
"""


def test():
    import pyre

    # declare a component
    class base(
        pyre.component, family="tests.components.validation", implements=pyre.protocol
    ):
        """
        The base component
        """

        # traits
        # a positive value
        positive = pyre.properties.float(default=0)

        # a value less than 1
        interval = pyre.properties.float(default=0)
        interval.validators = [pyre.constraints.isLess(value=1)]

        # attach a validator to multiple traits
        @staticmethod
        @pyre.descriptors.validator(traits=[positive, interval])
        def isPositive(value, **kwds):
            # build the constraint
            constraint = pyre.constraints.isPositive()
            # and enforce it
            return constraint.validate(value=value, **kwds)

    # instantiate
    b = base(name="b")

    # make an assignment that violates the constraint
    b.positive = -1
    # attempt to
    try:
        # read the value
        b.positive
        # this should be unreachable
        assert False
    # if the violation were detected correctly
    except b.ConstraintViolationError:
        # move on
        pass

    # make another assignment that violates the constraint
    b.interval = -0.5
    # attempt to
    try:
        # read the value
        b.interval
        # this should be unreachable
        assert False
    # if the violation were detected correctly
    except b.ConstraintViolationError:
        # move on
        pass

    # make another assignment that violates the constraint
    b.interval = 1
    # attempt to
    try:
        # read the value
        b.interval
        # this should be unreachable
        assert False
    # if the violation were detected correctly
    except b.ConstraintViolationError:
        # move on
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file
