#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the family names of the servers, the clients and the standard SQL mill: each is filed
under a plural noun, with the name of the implementation last
"""


def test():
    """
    Check the family of each protocol and component of the package
    """
    # access the package
    import pyre.db

    # each protocol or component, and its family
    families = [
        # the protocol of the data stores
        (pyre.db.datastore, "pyre.db.servers"),
        # the servers
        (pyre.db.postgres, "pyre.db.servers.postgres"),
        (pyre.db.sqlite, "pyre.db.servers.sqlite"),
        (pyre.db.backup, "pyre.db.servers.backup"),
        # the clients of the data stores
        (pyre.db.client, "pyre.db.clients"),
        # the mill that speaks standard SQL
        (pyre.db.sql, "pyre.db.dialects.standard"),
        # and the dialects of the back ends
        (pyre.db.backends.postgres.mill, "pyre.db.dialects.postgres"),
        (pyre.db.backends.sqlite.mill, "pyre.db.dialects.sqlite"),
    ]
    # go through them
    for entity, family in families:
        # and check each one
        assert entity.pyre_family() == family, (entity, entity.pyre_family())
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
