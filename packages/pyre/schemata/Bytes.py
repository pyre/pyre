# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Schema import Schema


# my declaration
class Bytes(Schema):
    """
    A type declarator for strings of octets, whose text is their hexadecimal digits
    """

    # constants
    typename = "bytes"  # the name of my type
    complaint = "could not coerce {0.value!r} into a string of octets"  # when i refuse

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a string of octets
        """
        # octets are octets
        if isinstance(value, bytes):
            # so pass them along
            return value
        # and so is anything else that holds them
        if isinstance(value, (bytearray, memoryview)):
            # in a copy that cannot change behind my back
            return bytes(value)
        # text is a string of hexadecimal digits, two per octet
        if isinstance(value, str):
            # attempt to
            try:
                # read the digits
                return bytes.fromhex(value)
            # if they are not hexadecimal digits
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
        # write the hexadecimal digits of the octets
        return value.hex()

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a string of octets
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onBytes
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=bytes(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
