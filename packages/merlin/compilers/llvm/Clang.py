# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin

# superclass
from .LLVM import LLVM


# the C compiler from the GNU compiler suite
class Clang(LLVM, family="merlin.compilers.llvm.clang"):
    """
    The C compiler from the LLVM compiler suite
    """

    # constants
    language = "c"

    # configurable state
    driver = merlin.properties.path()
    driver.default = "clang"


# end of file