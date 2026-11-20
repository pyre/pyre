# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import uuid

# superclass
from .Schema import Schema


# my declaration
class UUID(Schema):
    """
    A type declarator for universally unique identifiers
    """

    # constants
    typename = "uuid"  # the name of my type
    complaint = "could not coerce {0.value!r} into a universally unique identifier"  # refusal

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a universally unique identifier
        """
        # perhaps {value} is already one
        if isinstance(value, uuid.UUID):
            # in which case just return it
            return value
        # text
        if isinstance(value, str):
            # strip it
            value = value.strip()
            # if there is nothing left
            if not value:
                # it is uninitialized
                return None
            # attempt to
            try:
                # read the identifier
                return uuid.UUID(value)
            # if the text is not one
            except ValueError as error:
                # complain, passing along the reason
                raise self.CastingError(value=value, description=self.complaint, error=error)
        # all other types are incompatible
        raise self.CastingError(value=value, description=self.complaint)

    def string(self, value):
        """
        Render {value} as a string that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # the canonical form, with its hyphens
        return str(value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a universally unique identifier
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onUUID
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=None, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
