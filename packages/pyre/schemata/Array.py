# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc

# superclass
from .Sequence import Sequence

# default schema
from .Float import Float

# the evaluator of text, and the ways it can fail
from ..calc.evaluation import evaluate, errors
from ..calc.exceptions import DisallowedNameError

# the errors of the framework, which an entry that fails to convert raises
from ..framework.exceptions import PyreError


# declaration
class Array(Sequence):
    """
    The array type declarator: nested tuples of the values of my {schema}, as deep as my {rank}
    and with the extents of my {shape}, each of which is no constraint when it is {None}
    """

    # constants
    typename = "array"  # the name of my type

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into an array, whole or not at all: every entry must convert, and the
        result must be rectangular and agree with my {rank} and {shape}
        """
        # text is evaluated first, and anything else is taken as it is
        candidate = self._evaluate(value=value) if isinstance(value, str) else value
        # build the array, and check it before handing it back
        return self._check(value=value, array=self._build(value=candidate, **kwds))

    def string(self, value):
        """
        Render {value} as text that reads back as the same array
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # render it in brackets, all the way down, so even an array of one entry reads back as
        # an array
        return self._text(value=value)

    def json(self, value):
        """
        Generate a JSON representation of {value}, with my entries rendered by my schema
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # render each level, all the way down to the entries
        return self._json(value=value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an array
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onArray
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, schema=Float(), rank=None, shape=None, **kwds):
        # chain up
        super().__init__(schema=schema, **kwds)
        # a rank, if there is one, is a positive whole number
        if rank is not None and (isinstance(rank, bool) or not isinstance(rank, int) or rank < 1):
            # and anything else is a mistake in the declaration
            self._firewall(message=f"the rank of an array must be a positive integer, not {rank!r}")
        # a shape, if there is one, is a sequence
        if shape is not None and not isinstance(shape, (tuple, list)):
            # of extents
            self._firewall(
                message=f"the shape of an array must be a sequence of extents, not {shape!r}"
            )
        # with at least one of them
        if shape is not None and not shape:
            # since an array has at least one axis
            self._firewall(message="the shape of an array must have at least one extent")
        # each of which is a whole number that is not negative, or {None} for any length
        if shape is not None and not all(self._extent(extent=extent) for extent in shape):
            # and anything else is a mistake in the declaration
            self._firewall(
                message=(
                    f"the extents of an array must be non-negative integers or None, not {shape!r}"
                )
            )
        # and when there are both a rank and a shape
        if rank is not None and shape is not None and len(shape) != rank:
            # they must agree
            self._firewall(
                message=f"an array of rank {rank} cannot have the shape {tuple(shape)!r}"
            )
        # save my rank
        self.rank = rank
        # and my shape
        self.shape = None if shape is None else tuple(shape)
        # all done
        return

    # implementation details
    def _evaluate(self, value):
        """
        Evaluate the text in {value}, with access to the builtins a setting may use
        """
        # drop the blanks around it
        text = value.strip()
        # text with nothing in it
        if not text:
            # is an empty array
            return ()
        # attempt to
        try:
            # get the interpreter to evaluate it
            candidate = evaluate(expression=text, context={})
        # if it uses a function or a name the value of a setting may not
        except DisallowedNameError as error:
            # say so, in words the user can act on
            raise self.CastingError(value=value, description=str(error), error=error)
        # if it fails in any of the ways an evaluation can
        except errors as error:
            # complain
            raise self.CastingError(
                value=value, description="could not evaluate {0.value!r}", error=error
            )
        # if all goes well, return the {candidate}
        return candidate

    def _build(self, value, **kwds):
        """
        Convert {value} into nested tuples of the values of my schema
        """
        # a map is not a sequence of its keys
        if isinstance(value, collections.abc.Mapping):
            # an empty one is an empty array, like an empty list, set or tuple
            if not value:
                # so hand one back
                return ()
            # one with entries is not an array
            raise self.CastingError(value=value, description=self.complaint + self.type)
        # a single value
        if not self._nested(entry=value):
            # is not an array either
            raise self.CastingError(value=value, description=self.complaint + self.type)
        # the entries that fail to convert
        failures = []
        # convert the levels, all the way down to the entries
        array = self._convert(value=value, failures=failures, **kwds)
        # if every entry converted
        if not failures:
            # hand back the array
            return array
        # otherwise, the whole value is refused, since dropping entries would change its shape
        refusal = self.CastingError(
            value=value, description="could not coerce {0.value!r} into an array: {0.reasons}"
        )
        # and the refusal says why each entry failed
        refusal.reasons = "; ".join(f"{entry!r}: {error}" for entry, error in failures)
        # complain
        raise refusal

    def _convert(self, value, failures, **kwds):
        """
        Convert {value}, a level of an array, into a tuple; entries that fail are recorded in
        {failures} and hold their places as {None}, so the shape of the array stays as it was
        """
        # make a pile
        level = []
        # go through the entries
        for entry in value:
            # a level below this one
            if self._nested(entry=entry):
                # is converted the same way
                level.append(self._convert(value=entry, failures=failures, **kwds))
                # and that is all
                continue
            # attempt to
            try:
                # convert an entry; my entries have no names of their own, so a component
                # class among them becomes an anonymous instance
                converted = self.schema.process(value=entry, incognito=True, anonymous=True, **kwds)
            # if the framework refuses it
            except PyreError as error:
                # remember why
                failures.append((entry, error))
                # and hold its place
                converted = None
            # add it to the pile
            level.append(converted)
        # hand back the level
        return tuple(level)

    def _check(self, value, array):
        """
        Check that {array}, converted from {value}, is rectangular and agrees with my rank and
        shape, and hand it back
        """
        # an empty array has any rank, and fits a shape whose first axis may be empty
        if not array and self.shape is not None and self.shape[0] not in (None, 0):
            # but no other
            raise self.CastingError(
                value=value,
                description=(
                    f"could not coerce {{0.value!r}} into an array of shape {self.shape!r}:"
                    " it is empty"
                ),
            )
        # an empty array that got this far
        if not array:
            # is fine
            return array
        # measure the array
        shape = self._measure(level=array)
        # entries that are not all of the same shape
        if shape is None:
            # do not make an array
            raise self.CastingError(
                value=value,
                description=(
                    "could not coerce {0.value!r} into an array: its entries are not all of the"
                    " same shape"
                ),
            )
        # a depth other than my rank
        if self.rank is not None and len(shape) != self.rank:
            # is refused
            raise self.CastingError(
                value=value,
                description=(
                    f"could not coerce {{0.value!r}} into an array of rank {self.rank}:"
                    f" its rank is {len(shape)}"
                ),
            )
        # extents other than those of my shape
        if self.shape is not None and not self._fits(shape=shape):
            # are refused
            raise self.CastingError(
                value=value,
                description=(
                    f"could not coerce {{0.value!r}} into an array of shape {self.shape!r}:"
                    f" its shape is {shape!r}"
                ),
            )
        # all good
        return array

    def _measure(self, level):
        """
        Compute the shape of {level}, an array or a part of one, or {None} if its entries are not
        all of the same shape
        """
        # an entry has no extents
        if not isinstance(level, tuple):
            # so its shape is empty
            return ()
        # measure the entries
        shapes = {self._measure(level=entry) for entry in level}
        # entries of different shapes, or one that is not rectangular itself
        if len(shapes) > 1 or None in shapes:
            # make a level that is not rectangular
            return None
        # an empty level
        if not shapes:
            # has its length, and nothing below it
            return (0,)
        # otherwise, prepend my length to the shape of my entries
        return (len(level),) + shapes.pop()

    def _fits(self, shape):
        """
        Check whether {shape} has as many axes as mine, and my extents wherever i give one
        """
        # a different number of axes
        if len(shape) != len(self.shape):
            # does not fit
            return False
        # otherwise, every extent must match, unless mine takes any length
        return all(mine is None or mine == theirs for mine, theirs in zip(self.shape, shape))

    def _nested(self, entry):
        """
        Check whether {entry} is a container, rather than a value an array can hold
        """
        # anything iterable other than text is
        return isinstance(entry, collections.abc.Iterable) and not isinstance(entry, str)

    def _extent(self, extent):
        """
        Check whether {extent} is a valid extent of a declared shape
        """
        # {None} takes any length, and otherwise an extent is a whole number that is not negative
        return extent is None or (
            isinstance(extent, int) and not isinstance(extent, bool) and extent >= 0
        )

    def _text(self, value):
        """
        Render {value}, an entry or a level of an array, as text, with levels in brackets
        """
        # an entry
        if not isinstance(value, tuple):
            # is rendered by my schema
            return self.schema.string(value)
        # a level goes in brackets, with its entries rendered the same way
        return "[" + ", ".join(self._text(value=entry) for entry in value) + "]"

    def _json(self, value):
        """
        Render {value}, an entry or a level of an array, as json
        """
        # an entry
        if not isinstance(value, tuple):
            # is rendered by my schema
            return self.schema.json(value)
        # a level is a tuple of its entries, rendered the same way
        return tuple(self._json(value=entry) for entry in value)

    def _firewall(self, message):
        """
        Report a mistake in the declaration of an array, which is the developer's to fix
        """
        # access the journal
        import journal

        # and complain
        raise journal.firewall("pyre.schemata").log(message)


# end of file
