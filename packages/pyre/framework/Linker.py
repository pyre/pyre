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
        codec = self.codecs[uri.scheme]
        # ask it to load the shelf and return it
        return codec.load(uri=uri, **kwds)


    def resolve(self, uri, **kwds):
        """
        Attempt to locate the component class specified by {uri}
        """
        # what should we try? don't be tempted to make this more dynamic by, say, initializing
        # {schemes} with the {codecs} keys; order is significant here, so is visiting codecs
        # that register themselves under multiple schemes only once...
        schemes = [uri.scheme] if uri.scheme else self.SCHEMES

        # for each loading strategy
        for scheme in schemes:
            # try to
            try:
                # locate the associated decoder
                codec = self.codecs[scheme]
            # if not there
            except KeyError:
                # construct the reason
                reason = "unknown scheme {!r}".format(scheme)
                # and complain
                raise self.BadResourceLocatorError(uri=uri, reason=reason)

            # clone the input {uri} so we don't disturb it; make sure the candidate has the
            # scheme we are currently attempting
            candidate = uri.clone(scheme=scheme)

            # ask the codec for a sequence of matching symbols
            yield from codec.locateSymbol(uri=candidate, **kwds)

        # out of ideas
        return


    # meta-methods
    def __init__(self, executive, **kwds):
        # chain up
        super().__init__(**kwds)

        # the map from uris to known shelves
        self.shelves = {}
        # initialize my codec index
        self.codecs = self.indexDefaultCodecs()
        # go through the set of registered codecs
        for codec in {codec for codec in self.codecs.values()}:
            # and prime each one
            codec.prime(linker=self)

        # nothing else
        return


    # implementation details
    def indexDefaultCodecs(self):
        """
        Initialize my codec index
        """
        # make an empty one
        index = collections.OrderedDict()

        # add the native codec
        from ..config.native import native
        native.register(index=index)

        # add the file loader
        from ..config.odb import odb
        odb.register(index=index)

        # all done
        return index


    # constants
    SCHEMES = [ 'vfs', 'import' ]


# end of file
