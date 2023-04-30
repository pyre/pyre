# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# the extensions to the primitive datatypes
from .Path import Path as path
from .PathHash import PathHash as pathhash
from .URI import URI as uri

# typing
import os
import typing

# my shorthand; use {Union} since PEP604 is not available before python 3.10
pathlike = typing.Union[os.PathLike, str]

# end of file
