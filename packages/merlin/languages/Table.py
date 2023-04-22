# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# a table with language specific configurations
class Table(
    merlin.component,
    family="merlin.languages.table",
    implements=merlin.protocols.languages.table,
):
    """
    A table of language specific configurations
    """

    # configurable state
    autogen = merlin.protocols.languages.autogen()
    autogen.doc = "Template expander configuration"

    c = merlin.protocols.languages.c()
    c.doc = "C configuration"

    cxx = merlin.protocols.languages.cxx()
    cxx.doc = "C++ configuration"

    cuda = merlin.protocols.languages.cuda()
    cuda.doc = "CUDA configuration"

    cython = merlin.protocols.languages.cython()
    cython.doc = "cython configuration"

    fortran = merlin.protocols.languages.fortran()
    fortran.doc = "FORTRAN configuration"

    python = merlin.protocols.languages.python()
    python.doc = "python configuration"

    # metamethods
    def __iter__(self):
        """
        Generate a sequence of the supported languages
        """
        # yield each one
        yield self.autogen
        yield self.c
        yield self.cxx
        yield self.cuda
        yield self.cython
        yield self.fortran
        yield self.python
        # all done
        return


# end of file
