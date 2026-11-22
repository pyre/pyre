# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Measure import Measure


# declaration
class Reference(Measure):
    """
    Representation of foreign keys
    """

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know what i am: a column that holds the values of my referent
        """
        # my referent knows
        return self.referent._pyre_identify(authority=authority, **kwds)

    # markers
    def onDelete(self, action):
        """
        Set the action to perform when the target record is deleted. See {pyre.db.actions} for
        details
        """
        # mark
        self._foreign.delete = action
        # enable chaining
        return self

    def onUpdate(self, action):
        """
        Set the action to perform when the target record is updated. See {pyre.db.actions} for
        details
        """
        # mark
        self._foreign.update = action
        # enable chaining
        return self

    # meta-methods
    def __init__(self, key=None, onDelete=None, onUpdate=None, **kwds):
        # chain up with the settings i share with every column
        super().__init__(**kwds)

        # set up my foreign key with the rest
        self._foreign = self.foreign(key=key, onDelete=onDelete, onUpdate=onUpdate)

        # get the field reference recorded by the foreign key
        reference = self._foreign.reference
        # if the reference mentions a field explicitly
        if reference.field is not None:
            # save it
            field = reference.field
        # otherwise, it refers to the primary key of its table
        else:
            # which i cannot follow
            raise NotImplementedError("NYI!")

        # store my referent
        self.referent = field

        # all done
        return


# end of file
