# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import re


# implementation details
class URI:

    # types
    from .exceptions import ParsingError


    # public data
    @property
    def uri(self):
        """
        Assemble a string from my parts
        """
        parts = []
        # if I have a scheme
        if self.scheme: parts.append('{}:'.format(self.scheme))
        # if I have an authority
        if self.authority: parts.append('//{}'.format(self.authority))
        # if I have an address
        if self.address: parts.append('{}'.format(self.address))
        # if I have a query
        if self.query: parts.append('?{}'.format(self.query))
        # if I have a fragment
        if self.fragment: parts.append('#{}'.format(self.fragment))
        # assemble and return
        return ''.join(parts)


    # interface
    @classmethod
    def parse(cls, value, scheme=None, authority=None, address=None):
        """
        Convert {value} into a {uri}
        """
        # parse it
        match = cls._regex.match(value)
        # if unsuccessful
        if not match:
            msg = 'unrecognizable URI {0.value!r}'
            raise cls.ParsingError(value=value, description=msg)

        # otherwise, extract the parts
        thescheme = match.group('scheme')
        theauthority = match.group('authority')
        theaddress = match.group('address')
        thequery = match.group('query')
        thefragment = match.group('fragment')
        # build a URI object and return it
        return cls(
            scheme=thescheme if thescheme is not None else scheme,
            authority=theauthority if theauthority is not None else authority,
            address=theaddress if theaddress is not None else address,
            query=thequery,
            fragment=thefragment
            )


    def clone(self):
        """
        Make a copy of me
        """
        return type(self)(
            scheme=self.scheme, authority=self.authority, address=self.address,
            query=self.query, fragment=self.fragment)


    # meta-methods
    def __init__(self, scheme=None, authority=None, address=None, query=None, fragment=None):
        # save my parts
        self.scheme = scheme
        self.authority = authority
        self.address = address
        self.query = query
        self.fragment = fragment
        # all done
        return


    def __add__(self, other):
        """
        Enable concatenations

        N.B.: this is not {join}; it just takes my string representation, adds {other} to the
        end, and attempts to parse the result as a {uri}
        """
        # if {other} is not a string
        if not isinstance(other, str):
            # i don't know what to do
            raise NotImplemented
        # otherwise, turn me into a string and add {other}
        new = str(self) + other
        # coerce that into a uri and return it
        return self.parse(new)


    def __str__(self):
        # easy enough
        return self.uri


    # implementation details
    _regex = re.compile(
        "".join(( # adapted from http://regexlib.com/Search.aspx?k=URL
                r"^(?=[^&])", # disallow '&' at the beginning of uri
                r"(?:(?P<scheme>[^:/?#]+):)?", # grab the scheme
                r"(?://(?P<authority>[^/?#]*))?", # grab the authority
                r"(?P<address>[^?#]*)", # grab the address, typically a path
                r"(?:\?(?P<query>[^#]*))?", # grab the query, i.e. the ?key=value&... chunks
                r"(?:#(?P<fragment>.*))?"
                )))


    __slots__ = ( 'scheme', 'authority', 'address', 'query', 'fragment' )


# end of file
