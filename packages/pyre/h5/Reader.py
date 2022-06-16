# -*- coding: utf-8 -*-


# superclass
from .File import File


# the base reader
class Reader(File):
    """
    The base reader for h5 products
    """


    # interface
    def open(self, path):
        """
        Access the h5 file at {path}
        """
        # set the mode and delegate
        return super().open(path=path, mode="r")


    def read(self, query=None, path=None):
        """
        Open the h5 file at {path} and read the information in {query}
        """
        # if the user doesn't have any opinions
        if query is None:
            # grab my schema and use it for guidance as to what to read from the file
            query = self.schema()

        # all done
        return query


# end of file
