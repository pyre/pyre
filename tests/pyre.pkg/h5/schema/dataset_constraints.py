#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that datasets carry a list of constraints and that {process} enforces them; groups
carry no value and therefore no constraints
"""


# the driver
def test():
    # support
    import pyre
    import pyre.constraints as constraints
    from pyre.constraints.exceptions import ConstraintViolationError

    # a strings dataset starts with an empty constraint list
    pile = pyre.h5.schema.strings()
    assert pile.constraints == []

    # decorate it: a subset of {"A", "B"}, and non-empty
    pile.constraints = [
        constraints.isSubset(choices={"A", "B"}),
        constraints.isNotEmpty(),
    ]

    # valid values pass through {process} unchanged
    assert pile.process(value=["A"]) == ["A"]
    assert pile.process(value=["A", "B"]) == ["A", "B"]

    # a value outside the set is rejected
    try:
        pile.process(value=["A", "C"])
        # we should not get here
        assert False, "expected a constraint violation for a non-subset value"
    except ConstraintViolationError:
        pass

    # an empty value is rejected
    try:
        pile.process(value=[])
        # we should not get here
        assert False, "expected a constraint violation for an empty value"
    except ConstraintViolationError:
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
