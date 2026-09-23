#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the launcher hands a host file to mpich the way it spells it
"""


def test():
    # access the framework
    import pyre

    # the launcher
    from mpi.Launcher import Launcher

    # and the flavor
    from pyre.externals.supported.mpi.MPICH import MPICH

    # a launcher over mpich, with a host file; the names keep it clear of the shells the
    # other drivers configure through {mpi.pfg}
    launcher = Launcher(
        name="launcher_hostfile_mpich",
        mpi=MPICH(name="launcher_hostfile_mpich.mpi"),
        hostfile="localhost",
    )
    # build the command line
    argv = launcher.buildCommandLine()
    # hydra takes it as {-f}; older releases refuse the openmpi spelling
    assert argv[argv.index("-f") + 1] == "localhost"
    # and no other spelling is present
    assert not {"--hostfile", "-f", "-machinefile"} - {"-f"} & set(argv)
    # all done
    return launcher


# main
if __name__ == "__main__":
    # do it...
    test()


# end of file
