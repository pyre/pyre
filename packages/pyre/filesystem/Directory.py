# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .File import File


class Directory(File):
    """
    Representation of local filesystem folders
    """


    # interface
    def isDirectory(self):
        """
        Quick check of whether this node represents a folder or not
        """
        return True


    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a directory
        """
        return explorer.onDirectory(self, **kwds)


# end of file 
