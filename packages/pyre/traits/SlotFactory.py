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

    # types
    from ..components.exceptions import ResolutionError, TraitValueError
    from ..constraints.exceptions import ConstraintViolationError
    from ..schemata.exceptions import SchemaError

    # the errors that mean my trait refused a value
    refusals = (SchemaError, ConstraintViolationError, ResolutionError)

    # interface
    def preprocess(self, value: object, **kwds) -> object:
        """
        Prepare {value} for storage in a slot of my trait
        """
        # ask the preprocessor of my trait
        return self._pre(value=value, **kwds)

    def postprocess(self, value: object, node, **kwds) -> object:
        """
        Turn {value}, read from the slot {node} of my trait, into a value of my trait; if my
        trait refuses it, raise a {TraitValueError} that names the trait whose value {node} holds
        """
        # attempt to
        try:
            # ask the postprocessor of my trait
            value = self._post(value=value, node=node, **kwds)
        # if my trait refused the value with a {TraitValueError}
        except self.TraitValueError as error:
            # if the {error} doesn't know yet the slot that holds the refused value
            if error.slot is None:
                # it is {node}
                error.slot = node
            # if the {error} doesn't know yet the target {trait}
            if error.trait is None:
                # it must be mine, so mark it
                self.attribute(error=error, node=node)
            # and let it through
            raise
        # if my trait refused the value any other way
        except self.refusals as error:
            # make a {TraitValueError} that carries the refusal
            refusal = self.TraitValueError(value=value, error=error)
            # remember the slot that holds the refused value
            refusal.slot = node
            # mark it with the trait name
            self.attribute(error=refusal, node=node)
            # and raise it in place of the refusal
            raise refusal from error
        # if all goes well, return the {value}
        return value

    def attribute(self, error: TraitValueError, node) -> None:
        """
        Record in {error} the name of the trait whose value the slot {node} holds and, unless
        {error} knows better, where the value was set
        """
        # use the name of my trait, in case {node} is not in the store
        error.trait = self.trait.name
        # get the key of {node}
        key = node.key
        # a slot outside the store
        if key is None:
            # has nothing more to say
            return
        # attempt to
        try:
            # look up its metadata
            info = self.pyre_nameserver.getInfo(key)
        # if there are none
        except KeyError:
            # there is nothing more to say either
            return
        # use the name of the trait in the store, which says whose trait it is
        error.trait = info.name
        # and, if the error does not know where it came from
        if error.locator is None:
            # point to where the value was set
            error.locator = info.locator
        # all done
        return

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
