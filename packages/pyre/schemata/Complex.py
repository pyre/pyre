# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc

# superclass
from .Number import Number


# declaration
class Complex(Number):
    """
    A type declarator for complex numbers
    """

    # constants
    typename = "complex"  # the name of my type
    complaint = "could not coerce {0.value!r} into a complex number"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a complex number
        """
        # start with {value} itself
        candidate = value
        # if it is text
        if isinstance(value, str):
            # evaluate it
            candidate = self.evaluate(value=value)
        # text, which is what the expression may have evaluated to
        if isinstance(candidate, str):
            # is the only part
            parts = (candidate,)
        # a map is not a complex number, even though its keys could be taken as its parts; in a
        # configuration file, it is most likely a macro that was not quoted
        elif isinstance(candidate, collections.abc.Mapping):
            # so complain
            raise self.CastingError(value=value, description=self.complaint)
        # any other iterable
        elif isinstance(candidate, collections.abc.Iterable):
            # holds the parts
            parts = tuple(candidate)
        # and anything else
        else:
            # is the only part
            parts = (candidate,)
        # a complex number must have parts; the constructor would make zero out of none
        if not parts:
            # so complain
            raise self.CastingError(value=value, description=self.complaint)
        # now we are ready to
        try:
            # let the constructor do its job
            number = complex(*parts)
        # if it can't make sense of the parts, or one of them is out of its range
        except (TypeError, ValueError, OverflowError) as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint, error=error)
        # if all goes well, return the {number}
        return number

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a complex number
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onComplex
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=complex(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
