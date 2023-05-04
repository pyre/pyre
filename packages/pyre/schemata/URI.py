# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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
    typename = "uri"  # the name of my type
    complaint = "could not coerce {0.value!r} into a URI"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a resource locator
        """
        # if {value} is one of mine
        if isinstance(value, self.locator):
            # leave it alone
            return value

        # force conversion to a string; this shouldn't fail, unless the {__str__} converter of
        # {value} is broken, in which case it is almost certain we have a bug...
        value = str(value)

        # collapse all internal spaces; they are not valid values anyway
        value = "".join(value.split())

        # attempt to coerce
        try:
            # by assuming it is a string
            return self.locator.parse(
                value.strip(),
                scheme=self.scheme,
                authority=self.authority,
                address=self.address,
            )
        # if anything goes wrong
        except Exception as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint)

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # meta-methods
    def __init__(
        self, default=locator(), scheme=None, authority=None, address=None, **kwds
    ):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # save my defaults
        self.scheme = scheme
        self.authority = authority
        self.address = address
        # all done
        return


# end of file
