# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# my superclass
from ..framework.Dashboard import Dashboard # access to the framework managers


# class declaration
class SlotFactory(Dashboard):
    """
    A factory of slots of a given trait
    """


    # meta-methods
    def __init__(self, trait, processor, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my parts
        self.trait = trait
        self.processor = processor
        # all done
        return


    def __call__(self, value, current=None, **kwds):
        """
        Make a slot for my client trait
        """
        # if the {value} is already a slot
        if isinstance(value, self.pyre_nameserver.node):
            # just return it
            new = value
        # if it is a string
        elif isinstance(value, str):
            # do whatever the trait specifies as the slot building factory for string input
            new = self.trait.macro(postprocessor=self.processor, value=value, **kwds)
        # anything else
        else:
            # is native to the trait
            new = self.trait.native(postprocessor=self.processor, value=value, **kwds)

        # if the existing slot is non trivial
        if current is not None:
            # replace it
            new.replace(obsolete=current)

        # all done
        return new


# end of file
