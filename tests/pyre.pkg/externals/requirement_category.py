#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A bare category requirement constrains nothing
"""


def test():
    """
    Parse a requirement that is just a category tag and verify it is trivial
    """
    # support
    import pyre.externals

    # parse a bare category
    bare = pyre.externals.requirement.parse("hdf5")
    # the category is harvested
    assert bare.category == "hdf5"
    # there are no selectors
    assert bare.selectors == ()
    # no exclusions
    assert bare.exclusions == ()
    # and no version clauses
    assert bare.clauses == ()
    # any flavor is admissible
    assert bare.admits(flavor="serial")
    # with or without class tags
    assert bare.admits(flavor="openmpi", tags=("parallel",))
    # and any version is acceptable
    assert bare.accepts(version="1.8.0")

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
