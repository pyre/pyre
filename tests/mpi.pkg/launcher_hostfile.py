#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the launcher passes a host file to {mpirun} only when one was configured
"""


def test():
    # access the framework
    import pyre

    # and the launcher
    from mpi.Launcher import Launcher

    # a launcher nobody configured; the name keeps it clear of the shells the other drivers
    # configure through {mpi.pfg}
    launcher = Launcher(name="launcher_hostfile")
    # build the command line
    argv = launcher.buildCommandLine()
    # without a host file, {mpirun} is not handed one; before this check the unset trait held
    # an empty path, which is truthy and spells the current directory, so every launch got
    # {--hostfile .} and {mpirun} refused it
    assert "--hostfile" not in argv
    # configure one
    launcher.hostfile = "localhost"
    # rebuild
    argv = launcher.buildCommandLine()
    # and it goes on the command line, as given
    assert argv[argv.index("--hostfile") + 1] == "localhost"
    # all done
    return launcher


# main
if __name__ == "__main__":
    # do it...
    test()


# end of file
