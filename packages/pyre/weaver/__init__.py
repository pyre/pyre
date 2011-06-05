# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
This package contains the machinery necessary to generate content in a variety of output formats.

The primary target is human readable formats, such source code for programming languages.
"""


# access to the main component in this package
from .Weaver import Weaver as newWeaver


# access to the known languages
from .C import C as c
from .CSh import CSh as csh
from .Cxx import Cxx as cxx
from .F77 import F77 as f77
from .F90 import F90 as f90
from .HTML import HTML as html
from .Make import Make as make
from .Perl import Perl as perl
from .Python import Python as python
from .Sh import Sh as sh
from .TeX import TeX as tex
from .XML import XML as xml


# end of file 
