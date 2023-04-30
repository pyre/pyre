# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# declaration
class MemoryInfo:
    """
    Information about the amount of visible memory
    """

    # N.B.: not all platforms can make these distinctions; we do our best
    available = 0       # the largest allocation request that is likely to succeed
    free = 0            # the amount of currently unused memory
    total = 0           # the amount of total physical memory installed on the machine


# end of file
