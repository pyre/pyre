# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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
    from ..primitives import path

    # constants
    typename = "uri"  # the name of my type
    complaint = "could not coerce {0.value!r} into a URI"  # what i say when i refuse a value

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a resource locator
        """
        # if {value} is one of mine
        if isinstance(value, self.locator):
            # leave it alone
            return value
        # text, numbers and paths name resources by their text, since a file may be named after
        # a number; a boolean is not one of them, even though python counts it as an integer
        if isinstance(value, bool) or not isinstance(value, (str, int, float, self.path)):
            # nothing else names a resource: not a map, empty or not, and not the repr of a
            # container
            raise self.CastingError(value=value, description=self.complaint)

        # get the text
        value = str(value)

        # attempt to coerce
        try:
            # by assuming it is a string; blanks inside it are kept, since they are part of the
            # names of the resources users type, and only the ones around it are dropped
            uri = self.locator.parse(
                value.strip(),
                scheme=self.scheme,
                authority=self.authority,
                address=self.address,
            )
        # if the parser does not recognize it
        except self.locator.ParsingError as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint, error=error)
        # if all goes well, return the {uri}
        return uri

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a uri
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onURI
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

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
