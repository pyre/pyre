# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# framework
import merlin


# publish
# the GNU compiler suite
@merlin.foundry(implements=merlin.protocols.compiler, tip="the GCC compiler suite")
def gnu():
    """
    The GCC compiler suite
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
    The the C compiler from the GCC compiler suite
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
    The the C++ compiler from the GCC compiler suite
    """
    # get the suite
    from .GXX import GXX
    # and publish it
    return GXX


# aliases that are not valid python identifiers
# end of file
