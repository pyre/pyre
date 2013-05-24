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


    # constants
    open = '[({'
    close = '])}'
    delimiter = ','

    typename = 'sequence' # the name of my type
    default = () # my default value


    # public data
    from .Object import Object as schema # my default type


    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a container
        """
        # string processing
        if isinstance(value, str):
            # strip opening and closing delimiters
            if value and value[0] in self.open: value = value[1:]
            if value and value[-1] in self.close: value = value[:-1]
            # if there is nothing left, we are done
            if not value: return
            # otherwise, split it using comma as the separator
            value = (entry.strip() for entry in value.split(self.delimiter))
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
    def __init__(self, default=default, schema=schema, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # save my schema
        self.schema = schema
        # all done
        return


# end of file 
