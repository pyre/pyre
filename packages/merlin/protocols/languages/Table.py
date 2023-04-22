# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# languages
from .Autogen import Autogen
from .C import C
from .CXX import CXX
from .CUDA import CUDA
from .Cython import Cython
from .FORTRAN import FORTRAN
from .Python import Python


# a table with language specific configurations
class Table(merlin.protocol, family="merlin.languages.table"):
    """
    A table of language specific configurations
    """

    # configurable state
    autogen = Autogen()
    autogen.doc = "template expander configuration "

    c = C()
    c.doc = "C configuration"

    cxx = CXX()
    cxx.doc = "C++ configuration"

    cuda = CUDA()
    cuda.doc = "CUDA configuration"

    cython = Cython()
    cython.doc = "cython configuration"

    fortran = FORTRAN()
    fortran.doc = "FORTRAN configuration"

    python = Python()
    python.doc = "python configuration"

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # publish the default implementation
        return merlin.languages.table


# end of file
