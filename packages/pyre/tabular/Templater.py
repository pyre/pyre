# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import itertools
import collections
from ..patterns.AttributeClassifier import AttributeClassifier


class Templater(AttributeClassifier):
    """
    Metaclass that inspects sheet declarations
    """


    # types
    from .Record import Record
    from .Measure import Measure
    from .Derivation import Derivation
    from ..algebraic.Node import Node
    from ..algebraic.Operator import Operator


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build a new worksheet record
        """
        # harvest the locally declared items
        localItems = []
        for itemName, item in cls.pyre_harvest(attributes, cls.Node):
            # check whether this item is an {Operator} instance
            if isinstance(item, cls.Operator):
                # and convert it to a Derivation
                item = cls.Derivation(expression=item)
            # record the name
            item.name = itemName
            # and add it to the pile
            localItems.append(item)

        # remove them from the attributes for now
        # we will replace them with intelligent accessors in __init__; see below
        for item in localItems: del attributes[item.name]

        # set up the attributes
        attributes["pyre_name"] = name
        attributes["pyre_localItems"] = tuple(localItems)
        
        # build the record
        sheet = super().__new__(cls, name, bases, attributes, **kwds)

        # now that the record is built, we can hunt down inherited items
        inheritedItems = []
        # iterate over my ancestors
        for base in reversed(sheet.__mro__[1:]):
            # narrow the search down to my instances, i.e. subclasses of Sheet
            if isinstance(base, cls):
                    # add the items from this ancestor
                    inheritedItems.extend(base.pyre_localItems)

        # build the tuple of all items
        sheet.pyre_items = tuple(inheritedItems + localItems)
        # build the tuple of all measures
        sheet.pyre_measures = tuple(
            item for item in sheet.pyre_items if isinstance(item, cls.Measure))
        # build the tuple of all derivations
        sheet.pyre_derivations = tuple(
            item for item in sheet.pyre_items if isinstance(item, cls.Derivation))

        # create the Record subclass that holds the data
        recordName = name + "_record"
        recordBases = (cls.Record, )
        recordAttributes = collections.OrderedDict((item.name, item) for item in sheet.pyre_items)
        recordType = type(recordName, recordBases, recordAttributes)

        # attach it to the sheet
        sheet.pyre_Record = recordType

        # return the class record
        return sheet


    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a newly minted worksheet class
        """
        # initialize the record
        # print("Templater.__init__: initializing a new sheet class")
        super().__init__(name, bases, attributes, **kwds)

        # storage for the indexed measure accessors
        indices = []

        # iterate over all the items
        for index, item in enumerate(self.pyre_items):
            # build the data accessor
            accessor = item.pyre_sheetColumnAccessor(index=index, sheet=self)
            if isinstance(accessor, self.pyre_indexedAccessor):
                indices.append(accessor)
            # and attach it
            setattr(self, item.name, accessor)

        # attach the tuple of primary keys
        self.pyre_primaries = tuple(indices)

        # and return
        return


    def __call__(self, **kwds):
        """
        Build a new sheet
        """
        # create the sheet
        # print("Templater.__call__: building a new sheet instance")
        sheet = super().__call__(**kwds)
        # initialize the primary keys
        for accessor in self.pyre_primaries:
            # install the associated keymap
            sheet.pyre_keymaps[accessor] = accessor.keymap(sheet=sheet, column=accessor.index)
            # otherwise
        # and return it
        return sheet


# end of file 
