# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import collections


# declaration
class Linker:
    """
    Class responsible for accessing components from a variety of persistent stores
    """


    # types
    from .exceptions import FrameworkError, ComponentNotFoundError, BadResourceLocatorError
    from ..schemata import uri


    # public data
    codecs = None
    shelves = None


    # support for framework requests
    def loadShelf(self, uri, **kwds):
        """
        Load the shelf specified by {uri}
        """
        # coerce the uri
        uri = self.uri().coerce(uri)
        # get the codec
        codec = self.schemes[uri.scheme]
        # ask it to load the shelf and return it
        return codec.load(uri=uri, **kwds)


    def resolve(self, uri, **kwds):
        """
        Attempt to locate the component class specified by {uri}
        """
        # if the {uri} has a scheme, we will find the associated codec and get it to interpret
        # the resolution request. if the {uri} has no scheme, we will hand the request to each
        # codec in the order they were registered
        try:
            # make the pile
            codecs = [ self.schemes[uri.scheme] ] if uri.scheme else self.codecs
        # and if the look up fails
        except KeyError:
            # it's because we don't recognize the scheme
            reason = "unknown scheme {!r}".format(scheme)
            # so complain
            raise self.BadResourceLocatorError(uri=uri, reason=reason)

        # go through the relevant codecs
        for codec in codecs:
            # and form a sequence of matching symbols
            yield from codec.locateSymbol(uri=uri, **kwds)

        # out of ideas
        return


    # meta-methods
    def __init__(self, executive, **kwds):
        # chain up
        super().__init__(**kwds)

        # the map from uris to known shelves
        self.shelves = {}
        # setup my default codecs and initialize my scheme index
        codecs, schemes = self.indexDefaultCodecs()
        # save them
        self.codecs = codecs
        self.schemes = schemes

        # go through the set of registered codecs
        for codec in codecs:
            # and prime each one
            codec.prime(linker=self)

        # nothing else
        return


    # implementation details
    def indexDefaultCodecs(self):
        """
        Initialize my codec index
        """
        # get the codecs i know about
        from ..config.odb import odb
        from ..config.native import native
        # put them in a pile
        codecs = [odb, native]

        # make an empty index
        schemes = collections.OrderedDict()
        # register the native codec
        native.register(index=schemes)
        # register the file loader
        odb.register(index=schemes)

        # all done
        return codecs, schemes


# end of file
