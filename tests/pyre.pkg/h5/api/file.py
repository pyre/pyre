#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Check that the file constructor is accessible and has the correct pedigree
"""


# the driver
def test():
    # support
    import pyre

    # get the class
    f = pyre.h5.api.file
    # sort its inheritance
    pedigree = f.mro()
    # check it
    assert pedigree == [
        pyre.h5.api.file,
        pyre.h5.api.group,
        pyre.h5.api.object,
        pyre.h5.api.location,
        pyre.h5.api.identifier,
        object,
    ]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
