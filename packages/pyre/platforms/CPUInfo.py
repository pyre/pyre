# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# externals
import platform


# declaration
class CPUInfo:
    """
    Accumulator of information about the CPUs available on a host
    """

    # keep it simple for now
    # the cpu type; python seems to get this right reliably
    architecture = platform.machine()

    sockets = 1  # the number of physical chips; a socket has cores
    cores = 1  # the number of cores per socket; a core has cpus
    cpus = 1  # the number of cpus per core; see {hyper-threading}

    # there are layers above this that could be captured:
    #     books, drawers, nodes
    # will look into these as pyre and its applications get ported to the multi-layer architectures


# end of file
