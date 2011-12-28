# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import os


# class declaration
class Walker:
    """
    Class that encapsulates listing the contents of a local directory
    """


    # exceptions
    from .exceptions import DirectoryListingError


    # interface
    def walk(self, path):
        """
        Assume {path} is a directory, get the names of its contents and iterate over them
        """
        # attempt
        try:
            # to get the contents
            return os.listdir(path)
        # if this fails
        except os.error as error:
            # raise a package specific exception
            raise self.DirectoryListingError(uri=path, error=error.strerror)


# end of file 
