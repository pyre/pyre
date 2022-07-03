# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved

# the extensions to the primitive datatypes
from .Path import Path as path
from .PathHash import PathHash as pathhash
from .URI import URI as uri

# typing
import os
# my shorthand
pathlike = os.PathLike | str

# end of file
