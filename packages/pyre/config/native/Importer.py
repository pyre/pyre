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
    def locateSymbol(self, client, scheme, specification, context, locator):
        """
        Locate and load the symbol that corresponds to the given {specification}; if
        {specification} is not sufficiently qualified to point to a unique location, use
        {context} to form candidates until one results in a loadable shelf that can resolve the
        {specification}
        """
        # {specification} should have two parts: a {package} and a {symbol}; the {symbol}
        # corresponds to the component factory we are looking for, the {package} is the
        # namespace to which it belongs
        package, symbol = self.parseAddress(specification)
        # if we got a {package}, use it
        if package:
            candidates = [package]
        # otherwise
        else:
            # construct a sequence of progressively less qualified namespaces out of the given
            # context
            candidates = (
                self.separator.join(context[:m]) for m in reversed(range(1, len(context)+1))
                )
        # just in case there are no candidates
        shelf = None
        # now, iterate over the candidate namespaces
        for namespace in candidates:
            # first, ask the client to normalize the address
            source = client.normalizeURI(scheme=scheme, address=namespace)
            # attempt to retrieve a previously loaded shelf using the normalized uri
            try:
                shelf = client.shelves[source]
            # if that failed
            except KeyError:
                # attempt to import {source} as a module
                try:
                    shelf = self.decode(source=namespace, locator=locator)
                # if this fails as well
                except self.DecodingError:
                    # try the next candidate
                    continue
                # we got the shelf; first register it with the client
                client.registerShelf(shelf=shelf, source=source)
                # both ways
                client.registerShelf(shelf=shelf, source=shelf.source)
            # now, attempt to lookup our {symbol}
            try:
                descriptor = shelf.retrieveSymbol(symbol)
            # if that fails, move on to the next candidate
            except shelf.SymbolNotFoundError:
                continue
            # success!
            return descriptor
                
        # if we get this far
        raise self.SymbolNotFoundError(shelf=shelf, symbol=symbol)


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
