#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a query the catalog cannot run surfaces as a filesystem error
"""


def test():
    # support
    import pyre.filesystem

    # attempt to
    try:
        # get the package the default engine relies on
        import earthaccess
    # if it is not installed
    except ImportError:
        # there is nothing to check
        return None

    # a filesystem whose query names a parameter the query builder does not know
    fs = pyre.filesystem.earthaccess(query={"bogus": 1})
    # attempt to
    try:
        # discover, which rejects the query before it reaches the network
        fs.discover()
    # if it complained the way it should
    except fs.SearchError as error:
        # check that the query is on record
        assert error.uri == {"bogus": 1}
        # and the underlying complaint is there
        assert isinstance(error.error, ValueError)
    # if it didn't complain
    else:
        # that's a bug
        assert False, "unreachable"

    # all done
    return fs


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
