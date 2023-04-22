# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the base language protocol
from .Language import Language as language

# supported languages
from .Autogen import Autogen as autogen
from .C import C as c
from .CXX import CXX as cxx
from .CUDA import CUDA as cuda
from .Cython import Cython as cython
from .FORTRAN import FORTRAN as fortran
from .Python import Python as python

# language configuration table
from .Table import Table as table


# end of file
