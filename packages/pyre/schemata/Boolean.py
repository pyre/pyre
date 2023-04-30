# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Number import Number


# declaration
class Boolean(Number):
    """
    A type declarator for booleans
    """

    # constants
    typename = "bool"  # the name of my type
    complaint = "could not coerce {0.value!r} to bool"

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a boolean
        """
        # native type
        if isinstance(value, bool):
            # pass through unchanged
            return value
        # anything else
        try:
            # must be convertible by my table
            return self.xlat[value.lower()]
        # if anything goes wrong
        except Exception as error:
            # it is an error
            raise self.CastingError(description=self.complaint, value=value)

    # meta-methods
    def __init__(self, default=True, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return

    # implementation details
    # strings recognized as booleans
    xlat = {
        "1": True,
        "y": True,
        "yes": True,
        "on": True,
        "t": True,
        "true": True,
        "0": False,
        "n": False,
        "no": False,
        "off": False,
        "f": False,
        "false": False,
        "": True,  # mere presence is considered true
    }


# end of file
