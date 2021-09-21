# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import re
import subprocess
# framework
import merlin
# superclass
from .GNU import GNU


# the FORTRAN compiler from the GNU compiler suite
class GFortran(GNU, family="merlin.compilers.gnu.gfortran"):
    """
    The FORTRAN compiler from the GNU compiler suite
    """


    # constants
    language = "fortran"

    # configurable state
    driver = merlin.properties.path()
    driver.default = "gfortran"


# end of file
