# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
from .. import units

# my superclass
from .Number import Number


# declaration
class Dimensional(Number):
    """
    A type declarator for quantities with units
    """

    # constants
    typename = "dimensional"  # the name of my type
    complaint = "could not coerce {0.value!r} into a dimensional quantity"

    # public data
    parser = units.parser()

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a dimensional
        """
        # quantities with units
        if isinstance(value, units.dimensional):
            # go right through
            return value

        # attempt to coerce strings
        try:
            # by invoking the {units} parser
            return self.parser.parse(value, context=self.context)
        # if anything whatsoever goes wring
        except Exception as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint, error=error)

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dimensional quantity
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDimensional
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=units.zero, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
