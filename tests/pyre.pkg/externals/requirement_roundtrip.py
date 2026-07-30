#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The full grammar composes, normalizes stably, and the parser is idempotent
"""


def test():
    """
    Parse a requirement that exercises every section and round trip it
    """
    # support
    import pyre.externals

    # get the parser
    requirement = pyre.externals.requirement

    # parse a specification with all three sections
    full = requirement.parse("hdf5[openmpi]>=1.14,<2")
    # the category is harvested
    assert full.category == "hdf5"
    # the selector section too
    assert full.selectors == ("openmpi",)
    # and the version clauses, in order
    assert full.clauses == ((">=", "1.14"), ("<", "2"))
    # the normalized form reads back the same
    assert str(full) == "hdf5[openmpi]>=1.14,<2"

    # exclusions render with their polarity marker
    assert str(requirement.parse("hdf5[parallel,!mpich]")) == "hdf5[parallel,!mpich]"

    # structured requirements pass through the parser untouched
    assert requirement.parse(full) is full

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
