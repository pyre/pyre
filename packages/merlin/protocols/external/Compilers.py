# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# parts
from .Compiler import Compiler


# a table with compiler choices for each supported language
class Compilers(merlin.protocol, family="merlin.compilers.table"):
    """
    A table with compiler choices for each supported language
    """

    # configurable state
    # autogen = Compiler()
    # autogen.doc = "template expander configuration "

    c = Compiler()
    c.doc = "C compiler"

    cxx = Compiler()
    cxx.doc = "C++ compiler"

    # cuda = Compiler()
    # cuda.doc = "CUDA compiler"

    # cython = Compiler()
    # cython.doc = "cython compiler"

    fortran = Compiler()
    fortran.doc = "FORTRAN compiler"

    # python = Compiler()
    # python.doc = "python compiler"

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # publish the default implementation
        return merlin.compilers.compilers


# end of file
