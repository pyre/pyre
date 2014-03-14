# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# declaration
class Shelf:
    """
    A symbol table built on top of a native python module
    """

    # N.B: shelves used to build their locators using the {__file__} attribute of modules;
    # unfortunately, this attribute is not set for all modules on all platforms, so it is not
    # reliable. this version just records the caller's locator


    # exceptions
    from ..exceptions import SymbolNotFoundError


    # public data
    uri = None
    module = None
    locator = None


    # interface
    def retrieveSymbol(self, symbol):
        """
        Retrieve {symbol} from this shelf
        """
        # if the {symbol} is exported by my module
        try:
            # grab and return it
            return getattr(self.module, symbol)
        # otherwise
        except AttributeError as error:
            # complain
            raise self.SymbolNotFoundError(shelf=self, symbol=symbol) from error
        # unreachable
        import journal
        raise journal.firewall('pyre.config.native').log("UNREACHABLE")


    # meta methods
    def __init__(self, module, uri, locator,  **kwds):
        super().__init__(**kwds)
        # record the module
        self.module = module
        # the {uri} that caused it to get loaded
        self.uri = uri
        # and the locator
        self.locator = locator
        # all done
        return


# end of file 
