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
    separator = '/'


    # interface
    def locateSymbol(self, client, scheme, specification, context, locator):
        """
        Locate and load the symbol that corresponds to the given {specification}; if
        {specification} is not sufficiently qualified to point to a unique location, use
        {context} to form candidates until one results in a loadable shelf that can resolve the
        {specification}
        """
        # get the fileserver from the executive
        fileserver = client.fileserver
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
            candidates = client.componentSearchPath(context=context)
        # and, just in case there are no candidates
        shelf = None
        # now, iterate over the candidates
        for filename in candidates:
            # ask the client to normalize the address
            source = client.normalizeURI(scheme=scheme, address=filename)
            # attempt to retrieve a previously loaded shelf using the normalized uri
            try:
                shelf = client.shelves[source]
            # if not there
            except KeyError:
                # ask it to open the file
                try:
                    location, stream = fileserver.open(scheme=scheme, address=filename)
                # if this fails
                except fileserver.GenericError:
                    # get the next candidate
                    continue
                # decode
                try:
                    shelf = self.decode(source=stream, locator=locator)
                # and if it fails
                except self.DecodingError:
                    # move on
                    continue
                # we got the shelf; first register it with the client
                client.registerShelf(shelf=shelf, source=source)
                # both ways
                client.registerShelf(shelf=shelf, source=location)
            # now attempt to look for our {symbol}
            try:
                descriptor = shelf.retrieveSymbol(symbol)
            # if that fails
            except shelf.SymbolNotFoundError:
                # move on to the next candidate
                continue
            # success!
            return descriptor
                
        # if we get this far
        raise self.SymbolNotFoundError(shelf=shelf, symbol=symbol)
                    

    def decode(self, source, locator):
        """
        Interpret {source} as an open stream, execute it, and place its contents into a shelf
        """
        # read the contents
        contents = source.read()
        # build a new shelf
        shelf = self.Shelf(locator=locator)
        # invoke the interpreter to parse its contents
        try:
            exec(contents, shelf)
        except Exception as error:
            raise self.DecodingError(
                codec=self, uri=locator.source, description=str(error),
                locator=locator) from error
        # and return the shelf
        return shelf


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        return


# end of file
