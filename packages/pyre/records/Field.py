# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclasses
from .Entry import Entry
from ..algebraic.Leaf import Leaf


# declaration
class Field(Leaf, Entry):
    """
    The base class for record entries
    """


    # interface
    def extract(self, stream):
        """
        Extract a value from {stream} and walk it through casting, conversion and validation.
        """
        # get the value from the {stream}, process it and return it
        return self.process(value=next(stream))


    def evaluate(self, stream, cache):
        """
        Compute my value by either returning a previous evaluation or by extracting an item
        from {stream} and processing it
        """
        # if  have computed my value before
        try:
            # retrieve it it
            value = cache[self]
        # otherwise
        except KeyError:
            # compute it
            value = self.extract(stream=stream)
            # cache it
            cache[self] = value

        # and return
        return value


# end of file 
