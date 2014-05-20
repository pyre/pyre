# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


class Loader:
    """
    Base class for strategies that build component descriptors from persistent stores
    """


    # types
    from ..schemata import uri
    from .exceptions import LoadingError


    # interface
    @classmethod
    def locateSymbol(cls, executive, uri, protocol, **kwds):
        """
        Locate and load the symbol that corresponds to the given {uri}; if {uri} is not
        sufficiently qualified to point to a unique location, use {protocol} to form candidates
        until one of them results in a loadable shelf that can resolve the specification
        """
        # we split the address part of the {uri} into a {package} and a {symbol}. The {symbol}
        # corresponds to the component class we are looking for. The {package} is the
        # specification for the symbol table to which it belongs. These symbol tables are
        # called {shelves} here, and each {Loader} subclass has its own definition. They are
        # supposed to map the name of the symbol to an actual python object

        # attempt to
        try:
            # split the address into a package and a symbol; this should be done by every
            # loader since isolating the {symbol} requires knowledge of the separator
            package, symbol = uri.address.rsplit(cls.separator, 1)
        # if that fails
        except ValueError:
            # if there is no protocol, we are done
            if not protocol: return
            # use the address itself as the symbol
            symbol = uri.address
            # the package will be filled out using the protocol family
            package = ''

        # convert the package specification into a uri
        package = cls.uri.locator(scheme=uri.scheme, address=package)

        # look for matching shelves; the {uri} may match more than shelf, so try them all until
        # we find one that contains our target {symbol}
        for shelf in cls.loadShelves(executive=executive,
                                     protocol=protocol, uri=package, symbol=symbol,
                                     **kwds):
            # got one; attempt to
            try:
                # look for our symbol 
                descriptor = shelf.retrieveSymbol(symbol)
            # if not there
            except shelf.SymbolNotFoundError:
                # not much to do; better luck with the next shelf
                continue
            # otherwise, success!
            yield descriptor

        # if there is no protocol to help out, give up
        if not protocol: return

        # now, for my next trick: attempt to interpret the symbol itself as a shelf
        try:
            # load it
            shelf = cls.load(executive=executive, uri=cls.uri().coerce(symbol))
        # if anything goes wrong
        except cls.LoadingError:
            # just ignore it
            pass
        # if loading succeeds
        else:
            # look through its implementors
            for implementor in executive.registrar.implementors[protocol]:
                # get its package
                package = implementor.pyre_package()
                # and yield ones whose package name matches our symbol
                if package and package.name == symbol: yield implementor
            
        # out of ideas
        return


    @classmethod
    def loadShelves(cls, executive, protocol, uri, symbol, **kwds):
        """
        Locate and load shelves for the given {uri}; if the {uri} is not sufficiently qualified
        to point to a unique location, use {protocol} to form plausible candidates.
        """
        # access the linker
        linker = executive.linker
        # use {protocol} to build a sequence of candidate locations
        candidates = cls.locateShelves(
            executive=executive, protocol=protocol, uri=uri, symbol=symbol, **kwds)
        # go through each of them
        for uri in candidates:
            # print("Loader.loadShelves: uri={.uri!r}".format(uri))
            # does this uri correspond to a known shelf
            try:
                # if yes, grab it
                shelf = linker.shelves[uri.uri]
                # print("    shelf {!r} previously loaded".format(uri.uri))
            # otherwise
            except KeyError:
                # print("    new shelf; loading")
                # attempt to 
                try:
                    # load it
                    shelf = cls.load(executive=executive, uri=uri)
                # if it fails
                except cls.LoadingError as error:
                    # print("      skipping: {}".format(error))
                    # move on to the next candidate
                    continue
                # if the shelf was loaded correctly, register it with the linker
                # print("      success; registering it with the linker")
                linker.shelves[uri.uri] = shelf
            # yield the shelf to my caller
            yield shelf
        # no more candidates
        return


# end of file 
