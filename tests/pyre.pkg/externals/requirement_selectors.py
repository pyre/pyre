#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Flavor selectors are answered by the flavor name or its class tags
"""


def test():
    """
    Parse a selector and verify the admission rules
    """
    # support
    import pyre.externals

    # parse a requirement with a flavor selector
    parallel = pyre.externals.requirement.parse("hdf5[parallel]")
    # the selector is harvested
    assert parallel.selectors == ("parallel",)
    # the flavor name itself can answer
    assert parallel.admits(flavor="parallel")
    # or a class tag published by the recipe
    assert parallel.admits(flavor="openmpi", tags=("parallel",))
    # flavors with no matching name fail
    assert not parallel.admits(flavor="serial")

    # multiple selectors must all be answered
    both = pyre.externals.requirement.parse("hdf5[parallel,openmpi]")
    # a selection answering both passes
    assert both.admits(flavor="openmpi", tags=("parallel",))
    # answering only one is not enough
    assert not both.admits(flavor="mpich", tags=("parallel",))

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
