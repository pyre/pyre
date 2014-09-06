# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import collections.abc # for container identification
# superclass
from .Schema import Schema


# declaration
class Sequence(Schema):
    """
    The base class for type declarators that are sequences of other types
    """


    # constants
    open = '[({'
    close = '])}'
    delimiter = ','
    typename = 'sequence' # the name of my type
    container = tuple # the default container i represent


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


    # meta-methods
    def __init__(self, default=container, schema=Schema(), **kwds):
        # adjust the default; carefully, so we don't all end up using the same global container
        # checking for {None} is not appropriate here; the user may want {None} as the default
        # value; we need a way to know that {default} was not supplied: use {list} as the
        # marker
        default = self.container() if default is self.container else default
        # chain up with my default
        super().__init__(default=default, **kwds)
        # save my schema
        self.schema = schema
        # all done
        return


# end of file 
