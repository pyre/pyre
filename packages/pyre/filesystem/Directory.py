# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# superclass
from .InfoStat import InfoStat
from .InfoFolder import InfoFolder


# class declaration
class Directory(InfoStat, InfoFolder):
    """
    Representation of local filesystem folders
    """


# end of file
