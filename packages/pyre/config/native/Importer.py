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


    # interface
    def decode(self, source, locator=None):
        """
        Interpret {source} as a module to be imported
        """
        # import the module
        try:
            module = __import__(source)
        except ImportError as error:
            raise self.DecodingError(
                codec=self, uri=source, locator=locator, description=str(error)) from error
        except SyntaxError as error:
            raise self.DecodingError(
                codec=self, uri=source, locator=locator, description=str(error)) from error
        # now look it up in the list of modules and return it
        return self.Shelf(module=sys.modules[source])


# end of file
