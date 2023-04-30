# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin


# the GNU compiler suite
class Suite(merlin.component,
            family="merlin.compilers.gnu", implements=merlin.protocols.compiler):
    """
    The GNU compiler suite
    """


# end of file
