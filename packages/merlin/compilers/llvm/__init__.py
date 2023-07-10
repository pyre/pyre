# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin


# publish
# the LLVM compiler suite
@merlin.foundry(
    implements=merlin.protocols.external.compiler, tip="the LLVM compiler suite"
)
def llvm():
    """
    The LLVM compiler suite
    """
    # get the suite
    from .Suite import Suite

    # and publish it
    return Suite


# the C compiler from the LLVM compiler suite
@merlin.foundry(
    implements=merlin.protocols.external.compiler,
    tip="the C compiler from the LLVM compiler suite",
)
def clang():
    """
    The C compiler from the LLVM compiler suite
    """
    # get the suite
    from .Clang import Clang

    # and publish it
    return Clang


# the C compiler from the LLVM compiler suite
@merlin.foundry(
    implements=merlin.protocols.external.compiler,
    tip="the C++ compiler from the LLVM compiler suite",
)
def clangxx():
    """
    The C++ compiler from the LLVM compiler suite
    """
    # get the suite
    from .ClangXX import ClangXX

    # and publish it
    return ClangXX


# end of file
