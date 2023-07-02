# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# a table with compiler choices for each supported language
class Compilers(
    merlin.component,
    family="merlin.compilers.table",
    implements=merlin.protocols.external.compilers,
):
    """
    A table of language specific configurations
    """

    # configurable state
    # autogen = merlin.protocols.external.compiler()
    # autogen.doc = "Template expander configuration"

    c = merlin.protocols.external.compiler()
    c.default = "gcc"
    c.doc = "C compiler"

    cxx = merlin.protocols.external.compiler()
    cxx.default = "gcc"
    cxx.aliases = {"c++"}
    cxx.doc = "C++ compiler"

    # cuda = merlin.protocols.external.compiler()
    # cuda.default = "nvcc"
    # cuda.doc = "CUDA compiler"

    # cython = merlin.protocols.external.compiler()
    # cython.default = "cython"
    # cython.doc = "cython compiler"

    fortran = merlin.protocols.external.compiler()
    fortran.default = "gfortran"
    fortran.doc = "FORTRAN compiler"

    # python = merlin.protocols.external.compiler()
    # python.default = "python3"
    # python.doc = "python compiler"

    # metamethods
    def __iter__(self):
        """
        Generate a sequence of the compiler choices
        """
        # yield each one
        # yield self.autogen
        yield self.c
        yield self.cxx
        # yield self.cuda
        # yield self.cython
        yield self.fortran
        # yield self.python
        # all done
        return


# end of file
