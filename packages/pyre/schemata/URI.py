# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# implementation details
class uri:

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
    def clone(self):
        """
        Make a copy of me
        """
        return type(self)(
            scheme=self.scheme, authority=self.authority, address=self.address,
            query=self.query, fragment=self.fragment)

    # meta methods
    def __init__(self, scheme=None, authority=None, address=None, query=None, fragment=None):
        # save my parts
        self.scheme = scheme
        self.authority = authority
        self.address = address
        self.query = query
        self.fragment = fragment
        # all done
        return

    def __str__(self):
        # easy enough
        return self.uri

    # implementation details
    __slots__ = ( 'scheme', 'authority', 'address', 'query', 'fragment' )


# externals
import re
# superclass
from .Type import Type


# the declaration
class URI(Type):
    """
    Parser for resource identifiers
    """


    # types
    locator = uri # save the implementation type
    from .exceptions import CastingError


    # constants
    typename = 'uri' # the name of my type
    default = locator() # my default value


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a internet address
        """
        # if {value} is one of mine
        if isinstance(value, self.locator):
            # leave it alone
            return value
        # if it is a string
        if isinstance(value, str):
            # parse it
            match = self._regex.match(value)
            # if successful
            if match:
                # extract the parts
                scheme = match.group('scheme')
                authority = match.group('authority')
                address = match.group('address')
                query = match.group('query')
                fragment = match.group('fragment')
                # build a URI object
                uri = self.locator(
                    scheme=self.scheme if scheme is None else scheme,
                    authority=self.authority if authority is None else authority,
                    address=self.address if address is None else address,
                    query=match.group('query'),
                    fragment=match.group('fragment')
                    )
                # and return it
                return uri
        # otherwise
        msg = 'unrecognizable URI {0.value!r}'
        raise self.CastingError(value=value, description=msg)


    def __init__(self, default=default, scheme=None, authority=None, address=None, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # save my defaults
        self.scheme = scheme
        self.authority = authority
        self.address = address
        # all done
        return


    # private data
    _regex = re.compile(
        "".join(( # adapted from http://regexlib.com/Search.aspx?k=URL
                r"^(?=[^&])", # disallow '&' at the beginning of uri
                r"(?:(?P<scheme>[^:/?#]+):)?", # grab the scheme
                r"(?://(?P<authority>[^/?#]*))?", # grab the authority
                r"(?P<address>[^?#]*)", # grab the address, typically a path
                r"(?:\?(?P<query>[^#]*))?", # grab the query, i.e. the ?key=value&... chunks
                r"(?:#(?P<fragment>.*))?"
                )))


# end of file 
