# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import re # for the parser
import socket


# the base class of internet addresses; useful for detecting address specifications that have
# already been cast to an address instance
class Address:
    """
    Base class for addresses

    This class is useful when attempting to detect whether a value has already been converted
    to an internet address.
    """

    # public data
    @property
    def value(self):
        raise NotImplementedError(
            "class {.__name__!r} must implement 'value'".format(type(self)))


class IPv4(Address):
    """
    Encapsulation of an ipv4 socket address
    """

    # public data
    family = socket.AF_INET
    host = ""
    port = 0

    @property
    def value(self):
        """
        Build the tuple required by {socket.connect}
        """
        return (self.host, self.port)

    # meta methods
    def __init__(self, host='', port=None, **kwds):
        # don't chain up; there are keys in {kwds} that are not meant for me
        self.host = host
        self.port = 0 if port is None else int(port)
        return

    def __str__(self):
        return "{!r}:{}".format(self.host, self.port)


class Unix(Address):
    """
    Unix domain sockets
    """

    # public data
    family = socket.AF_UNIX
    path = None

    @property
    def value(self):
        """
        Build the value expected by {socket.connect}
        """
        return self.path

    # meta methods
    def __init__(self, path, **kwds):
        # don't chain up; there are keys in {kwds} that are not meant for me
        self.path = path
        return

    def __str__(self):
        return self.path


# the schema type superclass
from .Type import Type


# declaration
class INet(Type):
    """
    A type declarator for internet addresses
    """

    # types
    from .exceptions import CastingError
    # the address base class 
    address = Address
    # the more specialized types
    ip = ip4 = ipv4 = IPv4 
    unix = local = Unix


    # constants
    any = ip(host='', port=0)


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a internet address
        """
        # {address} instances go right through
        if isinstance(value, cls.address):
            return value
        # use the address parser to convert strings
        if isinstance(value, str):
            return cls.parse(value)
        # everything else is an error
        msg="could not convert {0.value!r} into an internet address"
        raise cls.CastingError(value=value, description=msg)


    @classmethod
    def recognize(cls, family, address):
        """
        Return an appropriate address type based on the socket family
        """
        # ipv4
        if family == socket.AF_INET:
            # unpack the raw address
            host, port = address
            # return an ipv4 addres
            return cls.ipv4(host=host, port=port)

        # unix
        if family == socket.AF_UNIX:
            # return a unix addres
            return cls.unix(path=address)

        # otherwise
        raise NotImplementedError("unsupported socket family: {}".format(family))


    @classmethod
    def parse(cls, value):
        """
        Convert {value}, expected to be a string, into an inet address
        """
        # interpret an empty {value}
        if not value:
            # as an ip4 address, on the local host at some random port
            return cls.ipv4()
        # attempt to match against my regex
        match = cls.regex.match(value)
        # if it failed
        if not match:
            # describe the problem
            msg = "could not convert {0.value!r} into an internet address"
            # bail out
            raise cls.CastingError(value=value, description=msg)
        # we have a match; get the address family
        family = match.group('ip') or match.group('unix')
        # if no family were specified
        if family is None:
            # build an ipv4 address
            return cls.ipv4(**match.groupdict())
        # otherwise, use it to find the appropriate factory to build and return an address
        return getattr(cls, family)(**match.groupdict())


    # support for building nodes
    @classmethod
    def macro(cls, model):
        """
        Return my preferred macro factory
        """
        # by default, i build interpolations
        return model.interpolation
    

    # private data
    regex = re.compile(
        r"(?P<unix>unix|local):(?P<path>.+)"
        r"|"
        r"(?:(?P<ip>ip|ip4|ip6|ipv4|ipv6):)?(?P<host>[^:]+)(?::(?P<port>[0-9]+))?"
        )


# end of file 
