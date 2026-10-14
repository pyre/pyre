# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Schema import Schema


# declaration
class Enum(Schema):
    """
    A type declarator for enums
    """

    # constants
    typename = "enum"  # the name of my type

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into an enum
        """
        # if the value is a string
        if isinstance(value, str):
            # attempt to
            try:
                # convert it to the enum value
                return self.enum[value]
            # if this fails
            except KeyError as error:
                # complain
                raise self.EnumError(enum=self.enum, value=value, error=error)
        # for all other types of value, we use the class converter
        try:
            # as provided by {__call__}
            return self.enum(value)
        # if anything goes wrong
        except ValueError as error:
            # complain
            raise self.EnumError(enum=self.enum, value=value, error=error)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an enumeration
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onEnum
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, enum, default=object, **kwds):
        # if the caller didn't provide a default value
        if default is object:
            # ask the {enum} for its zeroth member
            default = tuple(enum.__members__.values())[0]
        # chain up with my default
        super().__init__(default=default, **kwds)
        # save the enum class
        self.enum = enum
        # all done
        return


# end of file
