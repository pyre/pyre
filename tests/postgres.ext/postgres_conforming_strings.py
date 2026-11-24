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
    the session has it on
    """
    # externals
    import os

    # access the package
    import pyre.db

    # start the session with backslashes as escapes, the way a server or a role may be set up
    os.environ["PGOPTIONS"] = "-c standard_conforming_strings=off"
    # connect
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
