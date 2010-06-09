# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Codec(object):
    """
    The base class for readers/writers of the pyre configuration files
    """


    # public data
    encoding = None # descnedants must specify this


    # interface
    def resolve(self, client, address, factory):
        """
        Request by a client to resolve an (address, factory name) pair into a callable that
        will be invoked to build instances of the coresponding object

        Typical use involves turning the request into a component factory as a step towards
        binding a facility to an instance of the user-specified component
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'resolve'".format(self))


    def encode(self, item, stream):
        """
        Build a representation of {item} in the current encoding and inject it into {stream}
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'encode'".format(self))
    

    def decode(self, configurator, stream, locator=None):
        """
        Injest {stream} and return the decoded contents
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'decode'".format(self))
    

    # exceptions
    from .exceptions import EncodingError, DecodingError


# end of file
