# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..Codec import Codec
from .Shelf import Shelf


class ODB(Codec):
    """
    This package contains the implementation of the native importer
    """


    # constants
    encoding = "odb"
    filesystem = None


    # interface
    def decode(self, source, locator=None):
        """
        Interpret {source} as a vnode that points to an odb file, open it and place its
        contents into a shelf
        """
        # place the {source} contents in a shelf
        shelf = Shelf.retrieveContents(filesystem=self.filesystem, source=source)
        # and return it
        return shelf
        

    def retrieveSymbol(self, shelf, symbol):
        """
        Retrieve {symbol} from an existing {shelf}
        """
        try:
            return shelf[symbol]
        except AttributeError as error:
            raise self.SymbolNotFoundError(codec=self, shelf=shelf, symbol=symbol) from error
        except TypeError as error:
            raise self.ShelfError(codec=self, shelf=shelf, symbol=symbol) from error


    # meta methods
    def __init__(self, filesystem, **kwds):
        super().__init__(**kwds)
        self.filesystem = filesystem
        return


# end of file
