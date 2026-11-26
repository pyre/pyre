#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Restarting a postgres cluster replaces the one left behind with a fresh one
"""


def test():
    """
    Leave a running cluster behind, restart it, and check that its server runs on a new cluster
    """
    # externals
    import tempfile

    # get the package
    import pyre.db

    # a cluster; the suite says where the server programs are
    cluster = pyre.db.backends.postgres.cluster(name="cluster")
    # its data live beside this driver, named after it
    cluster.data = "cluster_restart"
    # its socket lives in a short directory of its own
    cluster.socket = tempfile.mkdtemp(prefix="pyre-")
    # and it need not survive a crash
    cluster.durable = False

    # make a cluster and start its server, as an earlier run that never finished would have
    cluster.init().start()
    # mark it, so the one that replaces it can be told apart
    marker = cluster.data / "leftover"
    # by leaving a file in its data directory
    marker.touch()

    # restart it
    cluster.restart()
    # check that its server runs
    assert cluster.status()
    # on a cluster other than the one left behind
    assert not marker.exists()

    # clean up
    cluster.remove()
    # and check that its data are gone
    assert not cluster.data.exists()
    # and so is the directory of its socket
    assert not cluster.socket.exists()

    # all done
    return cluster


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
