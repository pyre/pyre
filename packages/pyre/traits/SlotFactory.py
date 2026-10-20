# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from ..framework.Dashboard import Dashboard  # access to the framework managers


# class declaration
class SlotFactory(Dashboard):
    """
    A factory of slots of a given trait
    """

    # get the identity value processor
    from ..schemata import identity

    # make a null value processor
    noop = identity().coerce

    # interface
    def preprocess(self, value: object, **kwds) -> object:
        """
        Prepare {value} for storage in a slot of my trait
        """
        # ask the preprocessor of my trait
        return self._pre(value=value, **kwds)

    def postprocess(self, value: object, **kwds) -> object:
        """
        Turn {value}, read from a slot of my trait, into a value of my trait
        """
        # ask the postprocessor of my trait
        return self._post(value=value, **kwds)

    # meta-methods
    def __init__(self, trait, pre=noop, post=noop, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my trait
        self.trait = trait
        # and its value processors, which my slots reach through {preprocess} and {postprocess}
        self._pre = pre
        self._post = post
        # all done
        return

    def __call__(self, value, current=None, **kwds):
        """
        Make a slot for my client trait
        """
        # if the {value} is already a slot
        if isinstance(value, self.pyre_nameserver.node):
            # just use it
            new = value
        # if it is a string
        elif isinstance(value, str):
            # do whatever the trait specifies as the slot building factory for string input
            new = self.trait.macro(
                preprocessor=self.preprocess, postprocessor=self.postprocess, value=value, **kwds
            )
        # anything else
        else:
            # is native to the trait
            new = self.trait.native(
                preprocessor=self.preprocess, postprocessor=self.postprocess, value=value, **kwds
            )

        # if the existing slot is non trivial
        if current is not None:
            # replace it
            new.replace(obsolete=current)

        # all done
        return new


# end of file
