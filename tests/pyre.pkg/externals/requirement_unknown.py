#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Versions that cannot be compared satisfy only trivial requirements
"""


def test():
    """
    Verify the policy for unknown versions
    """
    # support
    import pyre.externals

    # get the parser
    parse = pyre.externals.requirement.parse

    # a requirement without version clauses accepts a version we can't compare
    assert parse("hdf5").accepts(version="unknown")
    # even an empty one
    assert parse("hdf5").accepts(version="")

    # a requirement with version clauses cannot be proven by an unknown version
    assert not parse("hdf5>=1.12").accepts(version="unknown")
    # nor by an empty one
    assert not parse("hdf5>=1.12").accepts(version="")

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
