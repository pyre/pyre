# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Number import Number


# declaration
class Integer(Number):
    """
    A type declarator for integers
    """

    # constants
    typename = "int"  # the name of my type
    complaint = "could not coerce {0.value!r} into an integer"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into an integer
        """
        # start with {value} itself
        candidate = value
        # if it is text
        if isinstance(value, str):
            # evaluate it
            candidate = self.evaluate(value=value)
        # otherwise, attempt to
        try:
            # let the constructor do its job; anything it accepts is fine
            number = int(candidate)
        # if it can't make sense of what it was given, or the {value} is out of its range
        except (TypeError, ValueError, OverflowError) as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint, error=error)
        # if all goes well, return the {number}
        return number

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an integer
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onInteger
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=int(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
