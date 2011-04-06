# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..Codec import Codec


class ODB(Codec):
    """
    This package contains the implementation of the native importer
    """

    
    # type
    from .Shelf import Shelf


    # constants
    encoding = "odb"


    # interface
    def decode(self, source, locator=None):
        """
        Interpret {source} as an open stream, execute it, and place its contents into a shelf
        """
        # read the contents
        contents = source.read()
        # build a new shelf
        shelf = self.Shelf()
        # invoke the interpreter to parse its contents
        try:
            exec(contents, shelf)
        except Exception as error:
            raise self.DecodingError(
                codec=self, uri=source.name, locator=locator, description=str(error)) from error
        # and return the shelf
        return shelf


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        return


# end of file
