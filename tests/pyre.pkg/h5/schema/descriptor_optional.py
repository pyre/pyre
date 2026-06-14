#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that descriptors can be marked optional, for both datasets and groups, and that
the marker defaults to {False}
"""


# the driver
def test():
    # support
    import pyre

    # a reusable subgroup
    class Sub(pyre.h5.schema.group):
        """
        A subgroup
        """

    # a group with required and optional members
    class Group(pyre.h5.schema.group):
        """
        A container with a mix of required and optional members
        """

        # a required scalar
        a = pyre.h5.schema.int()
        # an optional scalar
        b = pyre.h5.schema.int(optional=True)
        # an optional subgroup
        sub = Sub(optional=True)

    # the required dataset is not optional by default
    assert getattr(Group, "a")._pyre_optional is False
    # the optional dataset is marked
    assert getattr(Group, "b")._pyre_optional is True
    # and so is the optional subgroup
    assert getattr(Group, "sub")._pyre_optional is True

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
