# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Folder import Folder
from . import _metaclass_Filesystem


class Filesystem(Folder, metaclass=_metaclass_Filesystem):
    """
    The base class for representing filesystems
    """


    # public data
    mountpoint = "/"


    # meta methods
    def __init__(self, **kwds):
        super().__init__(filesystem=self, **kwds)
        return


    # debugging support
    def _dump(self):
        """
        Print out my contents using a tree explorer
        """
        # build the explorer
        from . import newTreeExplorer
        explorer = newTreeExplorer()
        # get the representation of my contents
        printout = explorer.explore(self)
        # dump it out
        if interactive:
            for line in printout:
                print(line)
        # and return the explorer to the caller
        return explorer
        

# end of file 
