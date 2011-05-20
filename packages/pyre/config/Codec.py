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


    # public data: descendants must specify these
    encoding = None 
    separator = None 


    # interface
    def resolve(self, client, address, factory):
        """
        Request by a client to resolve an (address, factory name) pair into a callable that
        will be invoked to build instances of the corresponding object

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
    

    def decode(self, source, locator=None):
        """
        Injest {stream} and return the decoded contents
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'decode'".format(self))


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


    # exceptions
    from .exceptions import EncodingError, DecodingError, ShelfError, SymbolNotFoundError


# end of file
