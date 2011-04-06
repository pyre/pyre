# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from pyre.framework.exceptions import PyreError


class MerlinError(PyreError):
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
