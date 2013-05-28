# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    def loadShelf(self, executive, uri):
        """
        Load the shelf specified by {uri}
        """
        # coerce the uri
        uri = self.uri().coerce(uri)
        # get the codec
        codec = self.codecs[uri.scheme]
        # get it load the shelf and return it
        return codec.load(executive=executive, uri=uri)
        

    def resolve(self, executive, client, uri, **kwds):
        """
        Attempt to locate the component class specified by {uri}
        """
        # what should we try?
        schemes = [uri.scheme] if uri.scheme else ['vfs', 'import']

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

            # clone the input {uri} so we don't disturb it
            candidate = uri.clone()
            # make sure the candidate has a scheme
            candidate.scheme = scheme

            # the codec is able to provide a sequence of matching symbols
            yield from codec.locateSymbol(executive=executive, client=client, uri=candidate, **kwds)

        # out of ideas
        return 


    # meta-methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize my codec index
        self.codecs = self._indexDefaultCodecs()
        # the map from uris to known shelves
        self.shelves = {}
        # all done
        return


    # implementation details
    def _indexDefaultCodecs(self):
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
        
        
# end of file 
