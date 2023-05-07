# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin


# the llvm compiler suite
class Suite(
    merlin.component,
    family="merlin.compilers.llvm",
    implements=merlin.protocols.external.compiler,
):
    """
    The LLVM compiler suite
    """


# end of file
