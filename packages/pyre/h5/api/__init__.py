# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# the local exceptions
from . import exceptions

# internals that mirror the h5 c++ hierarchy
from .Identifier import Identifier as identifier
from .Location import Location as location
from .Object import Object as object

# publicly visible factories
from .Group import Group as group
from .Dataset import Dataset as dataset
from .Datatype import Datatype as datatype
from .File import File as file

# infrastructure
from .Inspector import Inspector as inspector

# visitors
from .Explorer import Explorer as explorer
from .Assembler import Assembler as assembler
from .Viewer import Viewer as viewer

# file access
from .Reader import Reader as reader
from .Writer import Writer as writer

# patch the inspector as a class attribute of groups
group._pyre_inspector = inspector()


# end of file
