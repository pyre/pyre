#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a launcher without an mpi installation refuses to spawn, and says how to point it
at one, instead of failing on a missing attribute
"""


def test():
    # access the framework
    import pyre

    # and the journal
    import journal

    # the launcher
    from mpi.Launcher import Launcher

    # a launcher with no mpi installation; the name keeps it clear of the shells the other
    # drivers configure through {mpi.pfg}
    launcher = Launcher(name="launcher_missing", mpi=None)
    # the refusal goes on this channel
    channel = journal.error("mpi.launcher")
    # capture it in a file
    log = "launcher_missing.log"
    channel.device = journal.file(path=log)
    # and keep it from raising, so the exit code can be checked
    channel.fatal = False
    # attempt to spawn
    status = launcher.spawn(application=None)
    # the launch is refused
    assert status == 1
    # and the entry names the problem and the remedy
    text = open(log, encoding="utf-8").read()
    assert "could not find an mpi installation" in text
    assert "mpi.shells.mpirun.mpi" in text
    assert "prefix:" in text
    # clean up
    import os

    os.remove(log)
    # all done
    return launcher


# main
if __name__ == "__main__":
    # do it...
    test()


# end of file
