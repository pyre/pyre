# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin
# superclass
from .GNU import GNU


# the C compiler from the GCC compiler suite
class GXX(GNU, family="merlin.compilers.gnu.g++"):
    """
    The C++ compiler from the GNU compiler suite
    """


    # constants
    language = "c++"

    # configurable state
    driver = merlin.properties.path()
    driver.default = "g++"


# end of file
