# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import collections # for the container protocols
# superclass
from .Type import Type


# declaration
class Sequence(Type):
    """
    The base class for type declarators that are sequences of other types
    """


    # public data
    from .Object import Object as identity # my default type
    

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a container
        """
        # string processing
        if isinstance(value, str):
            # strip opening and closing delimiters
            if value and value[0] in '[({': value = value[1:]
            if value and value[-1] in '])}': value = value[:-1]
            # if there is nothing left, we are done
            if not value: return
            # otherwise, split it using comma as the separator
            value = (entry.strip() for entry in value.split(','))
        # if we have an iterable
        if isinstance(value, collections.Iterable):
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


    # meta-methods
    def __init__(self, schema=identity, **kwds):
        super().__init__(**kwds)
        self.schema = schema
        return


# end of file 
