# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Folder import Folder
from . import _metaclass_Filesystem


class Filesystem(Folder, metaclass=_metaclass_Filesystem):
    """
    The base class for representing filesystems
    """


    # public data
    mountpoint = "/"


    # interface
    def open(self, node, **kwds):
        """
        Open the file
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'open'".format(self))


    def sync(self):
        """
        Populate the filesystem by reading the external source it represents
        """
        return self


    # meta methods
    def __init__(self, root='/', **kwds):
        super().__init__(filesystem=self, **kwds)
        return


    # debugging support
    def _dump(self, interactive=True):
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


    # exceptions
    from .exceptions import GenericError
        

# end of file 
