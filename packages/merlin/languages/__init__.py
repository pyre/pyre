# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# source encodings
@merlin.components.language(language="autogen", tip="templates for generating source code")
def autogen():
    """
    The category of source artifacts that are expanded into other sources
    """
    # get the language
    from .Autogen import Autogen
    # and publish it
    return Autogen


@merlin.components.language(language="c", tip="the C language")
def c():
    """
    The category of source artifacts encoded in the C programming language
    """
    # get the language
    from .C import C
    # and publish it
    return C


@merlin.components.language(language="cuda", tip="the CUDA language")
def cuda():
    """
    The category of source artifacts encoded in the CUDA programming language
    """
    # get the language
    from .CUDA import CUDA
    # and publish it
    return CUDA


@merlin.components.language(language="c++", tip="the C++ language")
def cxx():
    """
    The category of source artifacts encoded in the C++ programming language
    """
    # get the language
    from .CXX import CXX
    # and publish it
    return CXX


@merlin.components.language(language="cython", tip="the cython language")
def cython():
    """
    The category of source artifacts encoded in the cython programming language
    """
    # get the language
    from .Cython import Cython
    # and publish it
    return Cython


@merlin.components.language(language="fortran", tip="the FORTRAN language")
def fortran():
    """
    The category of source artifacts encoded in the FORTRAN programming language
    """
    # get the language
    from .FORTRAN import FORTRAN
    # and publish it
    return FORTRAN


@merlin.components.language(language="python", tip="the Python language")
def python():
    """
    The category of source artifacts encoded in the Python programming language
    """
    # get the language
    from .Python import Python
    # and publish it
    return Python


# end of file
