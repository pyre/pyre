# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# superclass
from .InfoStat import InfoStat
from .InfoFolder import InfoFolder


# class declaration
class Directory(InfoStat, InfoFolder):
    """
    Representation of local filesystem folders
    """


# end of file
