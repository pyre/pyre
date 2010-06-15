# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import sys
from ..Codec import Codec


class Importer(Codec):
    """
    This package contains the implementation of the native importer
    """


    # constants
    encoding = "import"


    # interface
    def decode(self, address):
        """
        Interpret {address} as a module to be imported
        """
        # import the module
        try:
            module = __import__(address)
        except ImportError as error:
            raise self.DecodingError(
                codec=self, uri=address, locator=None, description=str(error)) from error
        # now look it up in the list of modules and return it
        return sys.modules[address]


# end of file
