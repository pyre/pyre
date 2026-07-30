#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Flavor exclusions rule selections out, even ones the selectors admit
"""


def test():
    """
    Parse exclusions and verify they override admission
    """
    # support
    import pyre.externals

    # parse a requirement with an exclusion
    notSerial = pyre.externals.requirement.parse("hdf5[!serial]")
    # the exclusion is harvested
    assert notSerial.exclusions == ("serial",)
    # the excluded flavor is inadmissible
    assert not notSerial.admits(flavor="serial")
    # everything else passes
    assert notSerial.admits(flavor="openmpi", tags=("parallel",))

    # selectors and exclusions mix
    mixed = pyre.externals.requirement.parse("hdf5[parallel, !mpich]")
    # an openmpi selection tagged parallel passes
    assert mixed.admits(flavor="openmpi", tags=("parallel",))
    # an mpich selection is ruled out even though it answers the selector
    assert not mixed.admits(flavor="mpich", tags=("parallel",))

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
