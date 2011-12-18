# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import sys
import pyre.tracking

# and ancestors
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
    def decode(self, client, scheme, source, locator):
        """
        Interpret {source} as a module to be imported
        """
        # build a locator for this request
        shelfLocator = pyre.tracking.newSimpleLocator(source=source)
        # adjust the locator
        locator = pyre.tracking.chain(this=shelfLocator, next=locator) if locator else shelfLocator

        # import the module
        try:
            module = __import__(source)
        # if {source} does not describe an actual module
        except ImportError as error:
            # report it as a decoding error
            raise self.DecodingError(
                codec=self, uri=source, locator=locator, description=str(error)) from error
        # other exceptions are probably related to the contents of the module, so let them
        # through to the user; on success, look up the {module} in the global list of modules
        # and return it dressed up as a shelf
        return self.Shelf(module=sys.modules[source], locator=locator)


    def shelfSearchPath(self, client, context):
        """
        Build a sequence of locations to look for {context} appropriate shelves
        """
        # convert {context} into a sequence of progressively more general package specifications
        return (self.separator.join(context[:m]) for m in reversed(range(1, len(context)+1)))


# end of file
