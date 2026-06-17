#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the metaclass harvests {dimension} descriptors into a bucket separate from a
group's members, and that dimensions are inherited across the class hierarchy
"""


# the driver
def test():
    # support
    import pyre

    # a group with a dimension and a regular member
    class Swaths(pyre.h5.schema.group):
        """
        A container that provides a shape dimension
        """

        # a shape dimension this group provides
        nlines = pyre.h5.schema.dimension()
        nlines.doc = "the number of azimuth lines"

        # a regular member
        zeroDopplerTime = pyre.h5.schema.int()

    # the dimension is harvested as a dimension, not a member
    assert "nlines" in Swaths._pyre_classDimensions
    assert "nlines" not in Swaths._pyre_classDescriptors
    # so it never enters the member alias map (the writer/find machinery won't see it)
    assert "nlines" not in Swaths._pyre_staticAliases

    # the member is a member, not a dimension
    assert "zeroDopplerTime" in Swaths._pyre_classDescriptors
    assert "zeroDopplerTime" not in Swaths._pyre_classDimensions

    # the dimension carries its documentation like any descriptor
    assert getattr(Swaths, "nlines").doc == "the number of azimuth lines"

    # dimensions are inherited and accumulate across the hierarchy
    class Frequency(Swaths):
        """
        Adds a per-frequency dimension
        """

        # a second dimension
        nsamples = pyre.h5.schema.dimension()

    # the subclass sees both the inherited and the local dimension
    assert "nlines" in Frequency._pyre_classDimensions
    assert "nsamples" in Frequency._pyre_classDimensions

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
