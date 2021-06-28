# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# source encodings
@merlin.foundry(implements=merlin.protocols.language, tip="the C language")
def c():
    """
    The category of source artifacts encoded in the C programming language
    """
    # get the language
    from .C import C
    # and publish it
    return C


@merlin.foundry(implements=merlin.protocols.language, tip="the CUDA language")
def cuda():
    """
    The category of source artifacts encoded in the CUDA programming language
    """
    # get the language
    from .CUDA import CUDA
    # and publish it
    return CUDA


@merlin.foundry(implements=merlin.protocols.language, tip="the cython language")
def cython():
    """
    The category of source artifacts encoded in the cython programming language
    """
    # get the language
    from .Cython import Cython
    # and publish it
    return Cython


@merlin.foundry(implements=merlin.protocols.language, tip="the C++ language")
def cxx():
    """
    The category of source artifacts encoded in the C++ programming language
    """
    # get the language
    from .CXX import CXX
    # and publish it
    return CXX


@merlin.foundry(implements=merlin.protocols.language, tip="the FORTRAN language")
def fortran():
    """
    The category of source artifacts encoded in the FORTRAN programming language
    """
    # get the language
    from .FORTRAN import FORTRAN
    # and publish it
    return FORTRAN


@merlin.foundry(implements=merlin.protocols.language, tip="the Python language")
def python():
    """
    The category of source artifacts encoded in the Python programming language
    """
    # get the language
    from .Python import Python
    # and publish it
    return Python


# end of file
