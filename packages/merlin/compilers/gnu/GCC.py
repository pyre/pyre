# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin

# superclasses
from ..base.C import C
from .GNU import GNU


# the C compiler from the GNU compiler suite
class GCC(C, GNU, family="merlin.compilers.gnu.gcc"):
    """
    The C compiler from the GNU compiler suite
    """

    # constants
    tag = "gcc"
    language = "c"

    # configurable state
    driver = merlin.properties.path()
    driver.default = "gcc"


# end of file
