# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# superclass
from .Schema import Schema


# the declaration
class URI(Schema):
    """
    Parser for resource identifiers
    """


    # types
    from .exceptions import CastingError
    from ..primitives import uri as locator


    # constants
    typename = 'uri' # the name of my type


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a resource locator
        """
        # if {value} is one of mine
        if isinstance(value, self.locator):
            # leave it alone
            return value
        # if it is a string
        if isinstance(value, str):
            # attempt to
            try:
                # get my basic type to parse it
                return self.locator.parse(
                    value, scheme=self.scheme, authority=self.authority, address=self.address)
            # if anything goes wrong
            except self.locator.ParsingError:
                # complain
                msg = 'unrecognizable URI {0.value!r}'
                raise self.CastingError(value=value, description=msg)

        # otherwise
        msg = 'unrecognizable URI {0.value!r}'
        raise self.CastingError(value=value, description=msg)


    # meta-methods
    def __init__(self, default=locator(), scheme=None, authority=None, address=None, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # save my defaults
        self.scheme = scheme
        self.authority = authority
        self.address = address
        # all done
        return


# end of file
