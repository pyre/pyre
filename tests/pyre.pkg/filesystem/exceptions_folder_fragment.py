#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The message of a {FolderError} names the node that is not a folder as a path, the way the user
would spell it
"""


def test() -> None:
    """
    Make a {FolderError} about a node named by a path, and check how its message spells it
    """
    # support
    import journal
    import pyre
    from pyre.filesystem.exceptions import FolderError

    # make a channel for what goes wrong
    channel = journal.firewall("pyre.tests.filesystem.exceptions")
    # the node that is not a folder, named by a path, as the lookup of a node reports it
    fragment = pyre.primitives.path("/startup/app")
    # make the error
    error = FolderError(uri="/startup/app/app.cfg", fragment=fragment, filesystem=None, node=None)
    # the message the user sees
    message = str(error)
    # must spell the node as a path
    if "'/startup/app' is not a folder" not in message:
        # if not, say so
        channel.line("the message does not name the node by its path")
        channel.indent()
        channel.line(f"message: {message}")
        channel.line("look in: filesystem/exceptions.py, FolderError.description")
        channel.outdent()
        # and complain
        channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
