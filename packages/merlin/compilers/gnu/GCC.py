# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin
# superclass
from .GNU import GNU


# the C compiler from the GNU compiler suite
class GCC(GNU, family="merlin.compilers.gnu.gcc"):
    """
    The C compiler from the GNU compiler suite
    """


    # constants
    language = "c"

    # configurable state
    driver = merlin.properties.path()
    driver.default = "gcc"


# end of file
