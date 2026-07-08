#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Sanity test: the chroma bindings are reachable through {pyre.libpyre}
    """
    # get the framework
    import pyre

    # there is nothing to check if the bindings were not built into this configuration
    if pyre.libpyre is None:
        # so quietly succeed
        return

    # reach the chroma bindings
    chroma = pyre.libpyre.chroma
    # the color type is present
    assert chroma.Color is not None
    # the {rgb} converters are present
    assert chroma.rgb is not None
    # the {ansi} serializers are present
    assert chroma.ansi is not None
    # the color palette is present
    assert chroma.rgb.palette is not None

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
