# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre.calc

# superclasses
from .Record import Record


# declaration
class DynamicRecord(Record):
    """
    Another base class for representing data extracted from persistent stores

    {DynamicRecord} uses a tuple of {pyre.calc} nodes for the value storage. This provides
    support for fields whose value can be changed. Derivations are setup with evaluators from
    {pyre.calc}.
    """


    # types
    from .Accessor import Accessor as pyre_fieldAccessor
    from .ConstAccessor import ConstAccessor as pyre_derivationAccessor


    # interface
    @classmethod
    def pyre_processFields(cls, raw, **kwds):
        """
        Form the tuple that holds my values by extracting information either from {raw} or
        {kwds}, and walking the data through casting, conversion and validation

        In the absence of derivations, the data tuple can be constructed by simply asking each
        field to consume one item from the raw input and convert it. We then build a
        pyre.calc.node to hold the value and place it in the output tuple
        """
        # if I were given an explicit tuple, build an iterator over it
        source = iter(raw) if raw is not None else (
            # otherwise, build a generator that extracts values from {kwds}
            kwds.pop(item.name, item.default) for item in cls.pyre_items)
        # build the data tuple and return it
        for item in cls.pyre_items:
            # construct the value
            value = item.eval(data=source)
            # build a calc node for it
            node = pyre.calc.newNode(value=value)
            # and yield it
            yield node
        # all  done
        return
        
            
    @classmethod
    def pyre_processFieldsAndDerivations(cls, raw, **kwds):
        """
        """
        # if I were given an explicit tuple, build an iterator over it
        source = iter(raw) if raw is not None else (
            # otherwise, build a generator that extracts values from {kwds}
            kwds.pop(item.name, item.default) for item in cls.pyre_items)
        # initialize the cache
        cache = {}
        # build the data tuple
        for item in cls.pyre_items:
            # get the item to compute its value
            value = item.eval(data=source, cache=cache)
            # if this item is a field, we have to convert the value into a calc node
            if isinstance(item, cls.Field):
                value = pyre.calc.newNode(value=value)
            # add it to the cache
            cache[item] = value
            # and yield t       he value
            yield value
        # all done
        return
            

    # meta methods
    # replace the methods in {tuple} with ones that are aware of the calc node interface
    def __getitem__(self, index):
        """
        Indexed read access: get the value of the associated node
        """
        return super().__getitem__(index).value


    def __setitem__(self, index, value):
        """
        Indexed write access: set the value of the associated node
        """
        super().__getitem__(index).value = value
        return


    def __iter__(self):
        """
        Build an iterator over my contents
        """
        # get my superclass to iterate over the nodes
        for node in super().__iter__():
            # dereference and yield
            yield node.value
        # all done
        return


    def __repr__(self):
        """
        Derefence my nodes to build a tuple with my values
        """
        # convert me into a tuple; this calls self.__iter__ implicitly
        return tuple(self)


    def __str__(self):
        """
        Build a string representation of my data
        """
        # build the string rep of my value tuple
        return str(self.__repr__())


# end of file 
