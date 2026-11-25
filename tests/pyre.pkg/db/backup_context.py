#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the backup server is its own context, and lets exceptions raised in it through
"""


# the exception raised inside the context
class Interruption(Exception):
    """
    Exception raised by the body of the context to check that it escapes
    """


def test():
    """
    Enter the context of a backup server, and raise an exception inside it
    """
    # support
    import io

    # access the package
    import pyre.db

    # make a backup server that writes its statements into a stream of its own
    server = pyre.db.backup(name="test", stream=io.StringIO())

    # check that the context
    try:
        # is the server itself
        with server as context:
            # say so
            assert context is server
            # and interrupt the body
            raise Interruption()
    # and that the exception escapes it
    except Interruption:
        # as it should
        pass
    # if it doesn't
    else:
        # complain
        assert False, "the exception did not escape the context"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
