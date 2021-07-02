# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# framework
import merlin


# the FORTRAN compiler from the GNU compiler suite
class GFortran(merlin.component,
          family="merlin.compilers.gnu.gfortran", implements=merlin.protocols.compiler):
    """
    The FORTRAN compiler from the GNU compiler suite
    """


# end of file
