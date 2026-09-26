#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Importing pyre loads no library of an optional package: the core stays independent of them
"""


def test():
    # support
    import os
    import pyre

    # the bindings are there
    assert pyre.libpyre is not None
    # the shared objects mapped into this process, on the hosts that say
    maps = "/proc/self/maps"
    # elsewhere there is nothing to check
    if not os.path.exists(maps):
        # so skip it
        return
    # read the map
    with open(maps) as stream:
        # the paths of the mapped files
        mapped = stream.read()
    # none of them is a cuda library
    for library in ("libcudart", "libcublas", "libcusolver", "libcurand", "libcuda."):
        # say which one showed up
        assert library not in mapped, f"'import pyre' loaded {library}"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
