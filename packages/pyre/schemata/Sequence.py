# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import collections.abc  # for container identification

# to get the base exception
import pyre

# superclass
from .Container import Container


# declaration
class Sequence(Container):
    """
    The base class for type declarators that are sequences of other types
    """

    # constants
    open = "[({"
    close = "])}"
    delimiter = ","
    typename = "sequence"  # the name of my type
    container = tuple  # the default container i represent
    complaint = "could not coerce {0.value!r} as a sequence"

    # interface
    def str(self, value):
        """
        Render value as a string that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            return None
        # my value knows
        return str(self.container(str(item) for item in value))

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # easy enough
        return self.container(str(item) for item in value)

    # implementation details
    def _coerce(self, value, incognito=True, **kwds):
        """
        Convert {value} into an iterable
        """
        # string processing
        if isinstance(value, str):
            # strip opening and closing delimiters
            if value and value[0] in self.open:
                value = value[1:]
            if value and value[-1] in self.close:
                value = value[:-1]
            # if there is nothing left
            if not value:
                # we are done
                return
            # otherwise, split it using comma as the separator
            value = filter(
                None, (entry.strip() for entry in value.split(self.delimiter))
            )
        # if we have an iterable
        if isinstance(value, collections.abc.Iterable):
            # go through each entry
            for entry in value:
                # attempt to
                try:
                    # convert it and hand it to the caller. perform the conversion incognito, in
                    # case coercing my values requires the instantiation of components; i don't
                    # want facilities to use the name of my node as the name of any instantiated
                    # components
                    yield self.schema.process(value=entry, incognito=incognito, **kwds)
                # if anything goes wrong that it is managed by the framework, assume it has
                # been communicated to the user
                except pyre.PyreError:
                    # and skip this entry
                    continue
            # all done
            return
        # otherwise, flag it as bad input
        raise self.CastingError(value=value, description=self.complaint)


# end of file
