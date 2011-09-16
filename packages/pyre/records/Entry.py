# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# super classes
from ..algebraic.Node import Node
from ..schema.Descriptor import Descriptor


# declaration
class Entry(Descriptor, Node):
    """
    The base class for record entries
    """


    # types
    # obligations from {pyre.algebraic} to support nodal algebra 
    @property
    def variable(self):
        """
        Grant access to the subclass used to encapsulate record fields
        """
        from .Field import Field
        return Field


    @property
    def operator(self):
        """
        Grant access to the subclass used encapsulate field operators
        """
        from .Derivation import Derivation
        return Derivation


    @property
    def literal(self):
        """
        Grant access to the subclass used encapsulate explicit constants
        """
        from .Literal import Literal
        return Literal


    # public data
    aliases = None # the set of names by which I am accessible


    # interface
    def extract(self, stream):
        """
        Extract a value from {stream} and walk it through casting, conversion and validation.
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'extract'".format(self))


    def evaluate(self, stream, cache):
        """
        Compute my value by either returning a previous evaluation or by extracting an item
        from {stream} and processing it
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'evaluate'".format(self))


    def process(self, value):
        """
        Convert {value} into an object that is consistent with my type and value requirements
        """
        # cast it
        value = self.type.pyre_cast(value)
        # convert it
        for converter in self.converters:
            value = converter(value)
        # validate it
        for validator in self.validators:
            value = validator(value)
        # and return it
        return value

        
    # meta methods
    def __init__(self, aliases=None, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)
        # initialize my aliases
        self.aliases = set() if aliases is None else aliases
        # all done
        return


# end of file 
