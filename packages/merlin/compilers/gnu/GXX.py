# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# framework
import merlin


# the C compiler from the GCC compiler suite
class GXX(merlin.component,
          family="merlin.compilers.gnu.g++", implements=merlin.protocols.compiler):
    """
    The C++ compiler from the GNU compiler suite
    """


# end of file
