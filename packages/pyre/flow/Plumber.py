# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# framework
import pyre

# local support
from .NameGenerator import NameGenerator


# declaration
class Plumber(pyre.actor):
    """
    The metaclass of flow nodes
    """

    # public data
    pyre_nameGenerator = NameGenerator()
    # whether the instances of my classes that were not named explicitly get a globally unique
    # name from my generator, rather than the name the framework would give them
    pyre_uniqueNames = False

    # metamethods
    def __call__(self, name=None, locator=None, implicit=False, **kwds):
        """
        Build an instance of one of my classes
        """
        # if unique names are on, and this instance was not named explicitly by the user
        if self.pyre_uniqueNames and (implicit or name is None):
            # build a unique name
            name = self.pyre_nameGenerator.uid()

        # if necessary, build a locator to reflect the construction site; the one {Actor} would
        # build would be wrong since it is now one level deeper in the stack
        locator = pyre.tracking.here(1) if locator is None else locator

        # create the instance
        instance = super().__call__(name=name, locator=locator, implicit=implicit, **kwds)
        # and return it
        return instance


# end of file
