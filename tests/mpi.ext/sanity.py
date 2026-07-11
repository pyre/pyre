#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the bindings module is present and loadable
"""


def test():
    # access the package that hosts the bindings
    import mpi

    # the extension module must have loaded; a {None} here means this machine has no mpi, and
    # this suite has no business running at all
    assert mpi.libmpi is not None

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
