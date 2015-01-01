# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


import pyre


class MerlinError(pyre.PyreError):
    """
    Base class for merlin exceptions
    """


class SpellNotFoundError(MerlinError):
    """
    Exception raised when the requested spell cannot be located
    """

    def __init__(self, spell, **kwds):
        msg = "spell {!r} not found".format(spell)
        super().__init__(description=msg, **kwds)
        self.spell = spell
        return


# end of file
