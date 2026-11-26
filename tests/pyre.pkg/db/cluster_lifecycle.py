#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A postgres cluster is made, its server starts and stops, and the cluster is removed
"""


def test():
    """
    Take a cluster through its life, and check its state after each step
    """
    # externals
    import tempfile

    # get the package
    import pyre.db

    # a cluster; the suite says where the server programs are
    cluster = pyre.db.backends.postgres.cluster(name="cluster")
    # its data live beside this driver, named after it
    cluster.data = "cluster_lifecycle"
    # its socket lives in a short directory of its own
    cluster.socket = tempfile.mkdtemp(prefix="pyre-")
    # and it need not survive a crash
    cluster.durable = False

    # take the cluster through its life
    try:
        # make the cluster
        cluster.init()
        # check that it is there
        assert cluster.initialized()
        # and that its server is not running yet
        assert not cluster.status()

        # start its server
        cluster.start()
        # check that it runs
        assert cluster.status()
        # and that it listens on its socket
        assert (cluster.socket / f".s.PGSQL.{cluster.port}").isSocket()

        # stop it
        cluster.stop()
        # check that it is gone
        assert not cluster.status()
        # and that the cluster is still there
        assert cluster.initialized()

        # remove the cluster
        cluster.remove()
        # check that its data are gone
        assert not cluster.data.exists()
        # and so is the directory of its socket
        assert not cluster.socket.exists()
    # and whatever the outcome of the checks
    finally:
        # leave no server running; a cluster that failed a check stays for inspection
        cluster.stop()

    # all done
    return cluster


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
