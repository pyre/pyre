# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc

# framework
from ..traits.Property import Property

# the trait descriptor for individual requirements
from .RequirementProperty import RequirementProperty


# the trait descriptor for lists of requirements
class Requirements(Property.list):
    """
    A trait descriptor for lists of package requirements

    Version conjunctions use the same comma that separates list entries, so splitting a
    text value must be grammar aware: a fragment that opens with a comparison operator
    continues the previous requirement rather than starting a new one. Malformed entries
    are reported, not silently dropped
    """

    # meta-methods
    def __init__(self, schema=None, **kwds):
        # requirements are the item type, unless the caller knows better
        schema = RequirementProperty() if schema is None else schema
        # chain up with it
        super().__init__(schema=schema, **kwds)
        # all done
        return

    # implementation details
    def _coerce(self, value, incognito=True, **kwds):
        """
        Convert {value} into a sequence of requirements
        """
        # text values must be split into individual specifications
        if isinstance(value, str):
            # requirements can't open with a bracket, so a leading one wraps the whole list
            if value and value[0] in self.open:
                # drop it
                value = value[1:]
                # along with its closing partner
                if value and value[-1] in self.close:
                    # from the other end
                    value = value[:-1]
            # split on the list delimiter and clean up the fragments
            fragments = (fragment.strip() for fragment in value.split(self.delimiter))
            # the repaired entries
            entries = []
            # go through the non-trivial fragments
            for fragment in filter(None, fragments):
                # a fragment that opens with a comparison operator is a version clause that
                # the split severed from the requirement before it
                if entries and fragment[0] in "<>=!":
                    # so glue it back on
                    entries[-1] = f"{entries[-1]},{fragment}"
                # anything else starts a new requirement
                else:
                    # so it stands alone
                    entries.append(fragment)
            # process the repaired entries
            value = entries
        # if by now we have an iterable
        if isinstance(value, collections.abc.Iterable):
            # go through each entry
            for entry in value:
                # convert it and hand it to the caller; unlike the generic sequence, a bad
                # entry raises: a requirement that vanishes silently subverts the resolver
                yield self.schema.process(value=entry, incognito=incognito, **kwds)
            # all done
            return
        # anything else is unusable; build the description
        description = self.complaint + self.type
        # and complain
        raise self.CastingError(value=value, description=description)


# end of file
