#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the result of a statement that a pipeline skipped raises an {OperationalError} when it
is checked, saying that the statement never ran and naming it
"""


def test():
    """
    Send a segment whose first statement fails through a pipeline, and check the one after it
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
        pipeline.execute("SELECT 2")
        # in a segment
        pipeline.sync()
        # read the results
        _, skipped = list(pipeline)
    # the second was skipped
    assert skipped.status == libpq.ExecStatus.pipelineAborted, skipped.status
    # and says so when it is checked
    try:
        # check it
        skipped.check("SELECT 2")
    # the failure
    except pyre.db.exceptions.OperationalError as error:
        # names the statement
        assert error.command == "SELECT 2", error.command
        # and says what happened to it
        assert error.diagnostic, "the failure did not say what happened"
    # a check that passes
    else:
        # means the skip was lost
        assert False, "the skip was not raised"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
