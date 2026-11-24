#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the result of a statement that fails in a pipeline raises the exception of the
condition the server named when it is checked, and that the statements after it in its segment
are reported as skipped
"""


def test():
    """
    Send a segment with a failing statement through a pipeline, and check the results
    """
    # access the package
    import pyre.db

    # and the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # in a pipeline
    with connection.pipeline() as pipeline:
        # a statement that divides by zero
        pipeline.execute("SELECT 1/0")
        # and one after it
        pipeline.execute("SELECT 1")
        # in a segment
        pipeline.sync()
        # read the results
        failed, skipped = list(pipeline)
    # the first failed
    assert not failed.ok
    # and says why when it is checked
    try:
        # check it
        failed.check("SELECT 1/0")
    # the failure
    except pyre.db.exceptions.DataError as error:
        # is the division by zero
        assert error.sqlstate == "22012", error.sqlstate
    # a check that passes
    else:
        # means the failure was lost
        assert False, "the failure was not raised"
    # and the second was skipped
    assert skipped.status == libpq.ExecStatus.pipelineAborted, skipped.status
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
