#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a pipeline sends its statements before any answer is read, and hands back their
results in order, as an iterator
"""


def test():
    """
    Send statements and prepared runs through a pipeline, and read their results
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # in a pipeline
    with connection.pipeline() as pipeline:
        # send a statement
        pipeline.execute("SELECT $1::integer", 1)
        # teach the server another
        pipeline.prepare("pyre_pipeline_double", "SELECT $1::integer * 2")
        # run it once
        pipeline.execPrepared("pyre_pipeline_double", 2)
        # and again
        pipeline.execPrepared("pyre_pipeline_double", 3)
        # and end the segment
        pipeline.sync()
        # four statements are waiting for their answers
        assert pipeline.pending == 4, pipeline.pending
        # read them
        results = list(pipeline)
    # the answers came in order: the statement
    assert results[0][0][0] == 1
    # the preparation
    assert results[1].ok
    # and the two runs
    assert [result[0][0] for result in results[2:]] == [4, 6]
    # and the session is out of the pipeline, and usable
    assert connection.exec("SELECT 1")[0][0] == 1
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
