# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import os


class DirectoryWalker:
    """
    Class that encapsulates listing the contents of a local directory
    """


    def walk(self, path):
        """
        Assume {path} is a directory, get the names of its contents and iterate over them
        """
        # get the contents
        try:
            return os.listdir(path)
        except os.error as error:
            raise self.DirectoryListingError(path=path, error=error.strerror)


    # exceptions
    from .exceptions import DirectoryListingError


# end of file 
