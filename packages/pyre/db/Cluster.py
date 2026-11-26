# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# packages
import pyre


# declaration
class Cluster(pyre.protocol, family="pyre.db.clusters"):
    """
    Protocol declaration for the managers of the database clusters a server runs on
    """

    # interface
    @pyre.provides
    def init(self):
        """
        Make the cluster, unless it exists already
        """

    @pyre.provides
    def start(self):
        """
        Start the server of the cluster, and wait until it accepts connections
        """

    @pyre.provides
    def stop(self):
        """
        Stop the server of the cluster
        """

    @pyre.provides
    def status(self):
        """
        Check whether the server of the cluster is running
        """

    @pyre.provides
    def remove(self):
        """
        Stop the server of the cluster, and delete the cluster
        """

    @pyre.provides
    def restart(self):
        """
        Replace whatever cluster is there with a fresh one, and start its server
        """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default cluster manager
        """
        # get the one for postgres
        from .backends.postgres.Cluster import Cluster

        # and hand it over
        return Cluster


# end of file
