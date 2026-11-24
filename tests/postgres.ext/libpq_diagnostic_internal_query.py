#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the diagnostic of a failed result carries the statement that a server-side function
built and ran, and where in it the server gave up
"""


def test():
    """
    Send a block that reads from a table that does not exist through a pipeline, and read the
    diagnostic of its result
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # in a pipeline, whose results come back without being checked
    with connection.pipeline() as pipeline:
        # a block that reads from a table that does not exist
        pipeline.execute("DO $$ BEGIN EXECUTE 'SELECT 1 FROM nowhere'; END $$")
        # in a segment
        pipeline.sync()
        # read the result
        (failed,) = list(pipeline)
    # the result failed
    assert failed.status == libpq.ExecStatus.fatalError, failed.status
    # get its diagnostic
    diagnostic = failed.diagnostic
    # which carries the statement the block ran
    assert diagnostic.internalQuery == "SELECT 1 FROM nowhere", diagnostic.internalQuery
    # and points at the name of the missing table in it
    assert diagnostic.internalPosition == 15, diagnostic.internalPosition
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
