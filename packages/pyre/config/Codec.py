# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Codec:
    """
    The base class for readers/writers of the pyre configuration files
    """

    
    # types
    # exceptions
    from .exceptions import EncodingError, DecodingError, ShelfError, SymbolNotFoundError


    # public data: descendants must specify these
    encoding = None 
    separator = None 


    # abstract interface
    def encode(self, item, stream):
        """
        Build a representation of {item} in the current encoding and inject it into {stream}
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'encode'".format(self))
    

    def decode(self, client, scheme, source, locator=None):
        """
        Injest {source} and return the decoded contents
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'decode'".format(self))


    def shelfSearchPath(self, client, context):
        """
        Build a sequence of locations to look for {context} appropriate shelves
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'shelfSearchPath'".format(self))


    # implemented interface
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
        # iterate over the locations in {specification}
        for shelf in self.locateShelves(client, scheme, package, context, locator):
            # attempt to look for our {symbol}
            try:
                descriptor = shelf.retrieveSymbol(symbol)
            # if that fails
            except shelf.SymbolNotFoundError:
                # move on to the next candidate
                continue
            # otherwise, success!
            yield descriptor
        # no more from me
        return


    def locateShelves(self, client, scheme, address, context, locator):
        """
        Locate and load shelves that correspond to the given {address}; if
        {address} is not sufficiently qualified to point to a unique location, use
        {context} to form plausible candidates. Returns an iterable of successfully loaded
        shelves
        """
        # if the address contained a valid {package}, use it; otherwise build a sequence
        # of candidate locations out of the given {context}
        candidates = [address] if address else self.shelfSearchPath(client=client, context=context)
        # now, iterate over the candidates
        for uri in candidates:
            # normalize the address
            source = self.normalizeURI(scheme=scheme, address=uri)
            # attempt to retrieve a previously loaded shelf using the normalized uri
            try:
                shelf = client.shelves[source]
            # if not there
            except KeyError:
                # attempt to create a new shelf by decoding the contents of {uri}
                try:
                    shelf = self.decode(client=client, scheme=scheme, source=uri, locator=locator)
                # and if it fails
                except self.DecodingError:
                    # move on
                    continue
                # we got the shelf; first register it with the client
                client.registerShelf(shelf=shelf, source=source)
            # and return it to my caller
            yield shelf
        # no more candidates
        return


    # uri utilities
    def normalizeURI(self, scheme=None, authority=None, address=None, query=None, symbol=None):
        """
        Construct a uri in normal form
        """
        # initialize the fragment container
        uri = []
        # handle the scheme
        if scheme is not None:
            uri.append(scheme + ":")
        # handle the authority
        if authority is not None:
            uri.append("//")
            uri.append(authority)
        # handle the address
        if address is not None:
            uri.append(address)
        # handle the query
        if query is not None:
            uri.append("?")
            uri.append(query)
        # handle the symbol
        if symbol is not None:
            uri.append("#")
            uri.append(symbol)
        # assemble and return
        return "".join(uri)


    def parseAddress(self, address):
        """
        Given an {address}, extract the package and factory parts
        """
        # split apart
        fields = address.split(self.separator)
        # the package is everything up to the last separator
        package = self.separator.join(fields[:-1])
        # and the symbol is the trailing part
        symbol = fields[-1]
        # return them to the caller
        return (package, symbol)


# end of file
