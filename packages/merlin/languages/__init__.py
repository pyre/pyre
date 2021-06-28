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


@merlin.foundry(implements=merlin.protocols.language, tip="the C++ language")
def cxx():
    """
    The category of source artifacts encoded in the C++ programming language
    """
    # get the language
    from .CXX import CXX
    # and publish it
    return CXX


# end of file
