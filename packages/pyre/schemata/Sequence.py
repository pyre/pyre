# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import collections.abc # for container identification
# superclass
from .Container import Container


# declaration
class Sequence(Container):
    """
    The base class for type declarators that are sequences of other types
    """


    # constants
    open = '[({'
    close = '])}'
    delimiter = ','
    typename = 'sequence' # the name of my type
    container = tuple # the default container i represent


    # implementation details
    def _coerce(self, value, **kwds):
        """
        Convert {value} into an iterable
        """
        # string processing
        if isinstance(value, str):
            # check for "nonw"
            if value.strip().lower() == "none": return None
            # strip opening and closing delimiters
            if value and value[0] in self.open: value = value[1:]
            if value and value[-1] in self.close: value = value[:-1]
            # if there is nothing left, we are done
            if not value: return
            # otherwise, split it using comma as the separator
            value = filter(None, (entry.strip() for entry in value.split(self.delimiter)))
        # if we have an iterable
        if isinstance(value, collections.abc.Iterable):
            # go through each entry
            for entry in value:
                # convert it and hand it to the caller. perform the conversion incognito, in
                # case coercing my values requires the instantiation of components; i don't
                # want facilities to use the name of my node as the name of any instantiated
                # components
                yield self.schema.coerce(value=entry, incognito=True, **kwds)
            # all done
            return
        # otherwise, flag it as bad input
        raise self.CastingError(value=value, description="unknown type: value={0.value!r}")


# end of file
