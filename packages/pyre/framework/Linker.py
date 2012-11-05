# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
    from ..schema import uri


    # public data
    codecs = None
    shelves = None


    # support for framework requests
    def loadShelf(self, executive, uri):
        """
        Load the shelf specified by {uri}
        """
        # coerce the uri
        uri = self.uri.coerce(uri)
        # get the codec
        codec = self.codecs[uri.scheme]
        # get it load the shelf and return it
        return codec.load(executive=executive, uri=uri)
        

    def retrieveComponentDescriptor(self, executive, facility, uri):
        """
        Attempt to locate the component class specified by {uri}
        """
        # print("Linker.retrieveComponentDescriptor:")
        # print("  uri: {!r}".format(uri))
        # print("  protocol: {}".format(facility.schema))
        # print("        shelves: {!r}".format(tuple(self.shelves.keys())))

        # get the nameserver
        nameserver = executive.nameserver
        # get the specified scheme
        scheme = uri.scheme
        # if there was no explicit scheme given
        if not scheme:
            # if we have anything explicitly registered under the address
            try:
                # get it
                yield nameserver[uri.address]
            # if not
            except nameserver.UnresolvedNodeError:
                # no problem
                pass

            # how about splicing the family name with the given address
            try:
                # get it
                yield nameserver[nameserver.join(facility.schema.pyre_family(), uri.address)]
            # if not
            except nameserver.UnresolvedNodeError:
                # no problem
                pass

        # what else should we try?
        schemes = [uri.scheme] if uri.scheme else ['import', 'vfs']
        # print("  schemes: {!r}".format(schemes))

        # for each loading strategy
        for scheme in schemes:
            # print("    attempting {!r}".format(scheme))
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

            # copy the input {uri}
            candidate = uri.clone()
            # make sure the candidate has a scheme
            candidate.scheme = scheme

            # the codec is able to provide a sequence of matching symbols
            for descriptor in codec.locateSymbol(
                executive=executive, facility=facility, uri=candidate):
                # got one! the facility will take care of the rest...
                # print("    candidate: {}".format(candidate))
                yield descriptor

        # if we get this far, everything we could think of has failed
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
