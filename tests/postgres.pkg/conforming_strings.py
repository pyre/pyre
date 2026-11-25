#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a session reads backslashes in text literals as ordinary characters, whatever the
server was told
"""


def test():
    """
    Ask the server to start the session with standard_conforming_strings off, attach, and check
    the session has it on; a server that refuses to read backslashes as escapes refuses such a
    session instead
    """
    # externals
    import os

    # access the package
    import pyre.db

    # connect as the server is set up
    probe = pyre.db.postgres(name="conforming_version").attach()
    # to learn which server this is
    version = probe.connection.server
    # and disconnect
    probe.detach()

    # start the session with backslashes as escapes, the way a server or a role may be set up
    os.environ["PGOPTIONS"] = "-c standard_conforming_strings=off"

    # a server from postgres 19 on reads backslashes as ordinary characters, always
    if version >= 190000:
        # carefully
        try:
            # it refuses a session that asks for them as escapes
            pyre.db.postgres(name="conforming").attach()
        # with the failure of the connection
        except pyre.db.exceptions.OperationalError:
            # which is what it should do
            pass
        # a session that starts
        else:
            # means the server took a setting it no longer has
            assert False, "the server accepted a session told to read backslashes as escapes"
        # all done
        return

    # the others accept the session
    db = pyre.db.postgres(name="conforming").attach()
    # ask for the setting
    ((setting,),) = db.execute("SHOW standard_conforming_strings")
    # it is the one the literals assume
    assert setting == "on", setting
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
