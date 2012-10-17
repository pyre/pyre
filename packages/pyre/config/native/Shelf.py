# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
from ... import tracking


# declaration
class Shelf:
    """
    A symbol table built on top of a native python module
    """


    # exceptions
    from ..exceptions import SymbolNotFoundError


    # public data
    uri = None
    module = None
    locator = None

    @property
    def source(self):
        """
        Return the filename associated with this module
        """
        return self.module.__file__


    # interface
    def retrieveSymbol(self, symbol):
        """
        Retrieve {symbol} from this shelf
        """
        try:
            return getattr(self.module, symbol)
        except AttributeError as error:
            raise self.SymbolNotFoundError(shelf=self, symbol=symbol) from error

        # unreachable
        import journal
        raise journal.firewall('pyre.config.native').log("UNREACHABLE")


    # meta methods
    def __init__(self, module, uri, locator,  **kwds):
        super().__init__(**kwds)
        self.module = module
        self.uri = uri
        self.locator = tracking.chain(this=tracking.file(source=module.__file__), next=locator)
        return


# end of file 
