# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Descriptor import Descriptor


# a named shape dimension
class Dimension(Descriptor):
    """
    A named shape dimension: a positive-integer extent that datasets reference by name in
    their {shape}

    A dimension is declared on the group that scopes it. Unlike datasets and subgroups, it
    is not file content: it is a shape parameter, resolved against the schema tree and bound
    to a reactive value at realization. The metaclass therefore harvests dimensions into a
    bucket separate from the group's members.
    """

    # decoration
    def _pyre_marker(self):
        """
        Generate an identifying mark for structural renderings
        """
        # easy
        return "dim"


# end of file
