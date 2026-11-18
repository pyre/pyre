#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the driver
def test():
    """
    Check that datasets carry a list of constraints and that {process} enforces them; groups carry
    no value and therefore no constraints
    """
    # support
    import pyre
    import pyre.constraints as constraints
    from pyre.constraints.exceptions import ConstraintViolationError

    # make a strings dataset
    pile = pyre.h5.schema.strings()
    # which starts with an empty constraint list
    assert pile.constraints == []

    # decorate it: a subset of {"A", "B"}, and non-empty
    pile.constraints = [
        constraints.isSubset(choices={"A", "B"}),
        constraints.isNotEmpty(),
    ]

    # valid values pass through {process} unchanged: a single choice
    assert pile.process(value=["A"]) == ["A"]
    # and both of them
    assert pile.process(value=["A", "B"]) == ["A", "B"]

    # a value outside the set
    try:
        # is processed
        pile.process(value=["A", "C"])
        # we should not get here
        assert False, "expected a constraint violation for a non-subset value"
    # and rejected
    except ConstraintViolationError:
        # as expected
        pass

    # an empty value
    try:
        # is processed
        pile.process(value=[])
        # we should not get here
        assert False, "expected a constraint violation for an empty value"
    # and rejected
    except ConstraintViolationError:
        # as expected
        pass

    # {None} is left alone, with no constraint check
    assert pile.process(value=None) is None

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
