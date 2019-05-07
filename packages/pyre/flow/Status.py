# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# support
import pyre


# declaration
class Status(pyre.tracker):
    """
    A helper that watches over a component's traits and records value changes
    """


    # interface
    def playback(self, node, alias):
        """
        Go through the history of the trait named {alias}
        """
        # find its trait by this name
        trait = node.pyre_trait(alias=alias)
        # get the key
        key = node.pyre_inventory[trait].key
        # chain up
        yield from super().playback(key=key)
        # all done
        return


    # meta-methods
    def __init__(self, node, **kwds):
        # chain up
        super().__init__(**kwds)
        # enable tracking
        self.track(component=node)
        # all done
        return


# end of file
