#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Sanity test: make sure the pyre extension is accessible
    """
    # access
    import pyre
    # verify the extension module exists
    assert pyre.libpyre, "extension module not found"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
