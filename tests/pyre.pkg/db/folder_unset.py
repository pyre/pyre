#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server without a folder refuses to attach, and names itself
"""


def test():
    """
    Attach a folder server that was given no folder
    """
    # access the package
    import pyre.db

    # make a server without a folder
    db = pyre.db.folder(name="folder_unset")
    # carefully
    try:
        # attach it
        db.attach()
    # it must be refused
    except pyre.db.exceptions.InterfaceError as error:
        # naming the server
        assert "folder_unset" in str(error), str(error)
    # if it is not
    else:
        # say so
        assert False, "a folder server without a folder attached"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
