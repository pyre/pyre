# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# get the framework
import pyre


# the base class for all merlin exceptions
class MerlinError(pyre.PyreError):
    """
    Base class for merlin exceptions
    """

# derived ones
class SpellNotFoundError(MerlinError):
    """
    Exception raised when the requested spell cannot be located
    """

    def __init__(self, spell, **kwds):
        # set up the message
        msg = "spell {.spell!r} not found"
        # chain up
        super().__init__(description=msg, **kwds)
        # save the missing spell name
        self.spell = spell
        # all done
        return


# end of file
