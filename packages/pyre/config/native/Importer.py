# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import sys
from ..Codec import Codec


class Importer(Codec):
    """
    This package contains the implementation of the native importer
    """

    
    # types
    from .Shelf import Shelf


    # constants
    encoding = "import"
    separator = '.'


    # interface
    def locateSymbol(self, specification, context, locator):
        """
        Locate and load the symbol that corresponds to the given {specification}; if
        {specification} is not sufficiently qualified to point to a unique location, use
        {context} to form candidates until one results in a loadable shelf that can resolve the
        {specification}
        """
        print("Importer.locateSymbol: client={!r}".format(self.client))
        # {specification} should have two parts: a {package} and a {symbol}; the {symbol}


    def decode(self, source, locator):
        """
        Interpret {source} as a module to be imported
        """
        # import the module
        try:
            module = __import__(source)
        except ValueError as error: # raise when {source} is empty
            raise self.DecodingError(
                codec=self, uri=source, locator=locator, description=str(error)) from error
        except ImportError as error:
            raise self.DecodingError(
                codec=self, uri=source, locator=locator, description=str(error)) from error
        except SyntaxError as error:
            raise self.DecodingError(
                codec=self, uri=source, locator=locator, description=str(error)) from error
        # now look it up in the list of modules and return it
        return self.Shelf(module=sys.modules[source], locator=locator)


# end of file
