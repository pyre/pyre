# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# superclass
from .Info import Info


# declaration
class InfoDirectory(Info):
    """
    Base class for encapsulating container meta-data for filesystem entries
    """

    # constants
    marker = 'd'
    isDirectory = True


    # interface
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a file
        """
        # dispatch
        return explorer.onFile(info=self, **kwds)


# end of file
