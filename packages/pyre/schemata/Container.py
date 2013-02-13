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
class Container(Type):
    """
    The base class for type declarators that are containers of others
    """


    # public data
    from .Object import Object as identity # my default type
    

    # interface
    def coerce(self, value, **kwds):
        """
        Covert {value} into a container
        """
        # string processing
        if isinstance(value, str):
            # strip opening and closing delimiters
            if value and value[0] in '[(': value = value[1:]
            if value and value[-1] in '])': value = value[:-1]
            # if there is nothing left, we are done
            if not value: return
            # otherwise, split it using comma as the separator
            value = (entry.strip() for entry in value.split(','))
        # if we have an iterable
        if isinstance(value, collections.Iterable):
            # go through each entry
            for entry in value:
                # convert it and hand it to the caller
                yield self.schema.coerce(value=entry, **kwds)
            # all done
            return
        # otherwise, flag it as bad input
        raise self.CastingError(value=value, description="unknown type: value={0.value!r}")


    # support for building nodes
    def macro(self, model):
        """
        Return my preferred macro factory
        """
        # ask my {schema} for its preference
        return self.schema.macro(model=model)
    

    # meta-methods
    def __init__(self, schema=identity, **kwds):
        super().__init__(**kwds)
        self.schema = schema
        return


# end of file 
