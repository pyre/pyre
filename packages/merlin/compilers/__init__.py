# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the table with compiler choices
from .Compilers import Compilers as compilers

# translate user friendly names to their canonical equivalents
aliases = {
    # compilers from the GNU suite
    "gcc": "gnu.gcc",
    "g++": "gnu.gxx",
    "gnu.g++": "gnu.gxx",
    "gfortran": "gnu.gfortran",
    # compilers from the llvm suite
    "clang": "llvm.clang",
    "clang++": "llvm.clangxx",
    "llvm.clang++": "llvm.clangxx",
}


# end of file
