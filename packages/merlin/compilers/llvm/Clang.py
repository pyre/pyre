# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin

# superclasses
from ..base.C import C
from .LLVM import LLVM


# the C compiler from the GNU compiler suite
class Clang(C, LLVM, family="merlin.compilers.llvm.clang"):
    """
    The C compiler from the LLVM compiler suite
    """

    # constants
    tag = "clang"
    language = "c"

    # configurable state
    driver = merlin.properties.path()
    driver.default = "clang"


# end of file
