# -*- coding: utf-8 -*-


# superclass
from .File import File


# the base writer
class Writer(File):
    """
    The base writer for h5 products
    """


    # interface
    def open(self, path, mode="a"):
        """
        Access the h5 file at {path}
        """
        # set the mode and delegate
        return super().open(path=path, mode=mode)


    def write(self, query, path=None):
        """
        Open the h5 file at {path} and write the information in {query}
        """
        # all done
        return query


# end of file
