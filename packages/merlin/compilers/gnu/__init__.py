# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin


# publish
# the GNU compiler suite
@merlin.foundry(implements=merlin.protocols.compiler, tip="the GNU compiler suite")
def gnu():
    """
    The GNU compiler suite
    """
    # get the suite
    from .Suite import Suite
    # and publish it
    return Suite


# the C compiler from the GNU compiler suite
@merlin.foundry(implements=merlin.protocols.compiler,
                tip="the C compiler from the GNU compiler suite")
def gcc():
    """
    The C compiler from the GNU compiler suite
    """
    # get the suite
    from .GCC import GCC
    # and publish it
    return GCC


# the C compiler from the GNU compiler suite
@merlin.foundry(implements=merlin.protocols.compiler,
                tip="the C++ compiler from the GNU compiler suite")
def gxx():
    """
    The C++ compiler from the GNU compiler suite
    """
    # get the suite
    from .GXX import GXX
    # and publish it
    return GXX


# the C compiler from the GNU compiler suite
@merlin.foundry(implements=merlin.protocols.compiler,
                tip="the FORTRAN compiler from the GNU compiler suite")
def gfortran():
    """
    The FORTRAN compiler from the GNU compiler suite
    """
    # get the suite
    from .GFortran import GFortran
    # and publish it
    return GFortran


# end of file
