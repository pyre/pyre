# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


"""
This package contains the machinery necessary to generate content in a variety of output formats.

The primary target is human readable formats, such source code for programming languages.
"""


# access to the main components in this package
from .Weaver import Weaver as weaver
# the language interface
from .Language import Language as language

# the mill base classes
from .Mill import Mill as mill
from .LineMill import LineMill as line
from .BlockMill import BlockMill as block

# access to the known languages
from .C import C as c
from .CSh import CSh as csh
from .Cfg import Cfg as cfg
from .Cxx import Cxx as cxx
from .F77 import F77 as f77
from .F90 import F90 as f90
from .HTML import HTML as html
from .Make import Make as make
from .Perl import Perl as perl
from .Python import Python as python
from .SQL import SQL as sql
from .SVG import SVG as svg
from .Sh import Sh as sh
from .TeX import TeX as tex
from .XML import XML as xml

# the templater
from .Smith import Smith as smith
# the protocol that captures the project metadata
from .Project import Project as project
# the templated project implementations
from .Django import Django as django
from .Plexus import Plexus as plexus


# end of file
