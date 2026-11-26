#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A postgres cluster whose server programs are not where it was told reports the missing one
"""


def test():
    """
    Point a cluster at a directory without the server programs, and check that making it fails
    """
    # get the journal
    import journal

    # and the package
    import pyre.db

    # a cluster
    cluster = pyre.db.backends.postgres.cluster(name="cluster")
    # whose server programs are in a directory that does not exist
    cluster.programs = "cluster_missing_initdb"
    # and whose data would live beside this driver, named after it
    cluster.data = "cluster_missing_initdb.data"

    # the missing program is expected, so its report goes to the trash rather than the console
    journal.error("pyre.db.cluster").device = journal.trash()
    # attempt to make the cluster
    try:
        # which fails
        cluster.init()
    # the failure is an error, and errors are fatal by default
    except journal.ApplicationError as error:
        # check that its entry names the missing program
        assert any("'initdb'" in line for line in error.page), error.page
    # anything else
    else:
        # is a failure
        assert False, "a cluster was made without initdb"
    # and nothing was made
    assert not cluster.data.exists()

    # all done
    return cluster


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
