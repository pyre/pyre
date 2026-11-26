# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .NamedTuple import NamedTuple


# declaration
class Immutable(NamedTuple):
    """
    Storage for and access to the values of immutable record instances
    """

    # exceptions
    from .exceptions import ImmutableFieldError

    # interface
    def pyre_observe(self, index, observer):
        """
        Let {observer} know of changes to the value at {index}; mine never change, so it will
        never hear from me
        """
        # all done
        return self

    # meta-methods
    def __setitem__(self, index, value):
        """
        Refuse to change the value at {index}, since my values are fixed when I am built
        """
        # find the record that lays me out
        record = self.pyre_layout
        # and refuse the change, naming the field that holds the value
        raise self.ImmutableFieldError(record=record, field=record.pyre_fields[index])

    # private data
    __slots__ = ()


# end of file
