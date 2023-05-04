# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Sequence import Sequence


# declaration
class Set(Sequence):
    """
    The set type declarator
    """

    # constants
    typename = "set"  # the name of my type
    container = set  # the container I represent

    # interface
    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # sets are not JSON representable, so we convert them into lists
        return self.list(str(item) for item in value)


# end of file
