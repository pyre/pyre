# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


import itertools
import collections
from ..records.Templater import Templater


class SheetMaker(Templater):
    """
    Metaclass that inspects sheet declarations
    """


    # types
    from .Index import Index as pyre_indexer
    from .Column import Column as pyre_accessor


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build a new worksheet record
        """
        # prime the name attribute; instances are given names by the user
        attributes["pyre_name"] = name
        # build the record
        sheet = super().__new__(cls, name, bases, attributes, **kwds)

        # create the row factory
        recordName = name + "_record"
        recordBases = (sheet.pyre_recordType, )
        recordAttributes = collections.OrderedDict((item.name, item) for item in sheet.pyre_entries)
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
        # print("SheetMaker.__init__: initializing a new sheet class")
        super().__init__(name, bases, attributes, **kwds)

        # build the list of primary fields
        # storage for the indexed measure accessors
        primaries = []
        # now, replace the regular column accessors with indexing accessors
        for measure in self.pyre_fields:
            # bail out if this is not an indexed measure
            if not measure.index: continue
            # create the data accessor 
            accessor = self.pyre_indexer(entry=measure, index=self.pyre_index[measure])
            # add it to the pile
            primaries.append(accessor)
            # and attach it
            setattr(self, measure.name, accessor)
        # attach the tuple of indexers
        self.pyre_primaries = primaries

        # all done
        return


    def __call__(self, **kwds):
        """
        Build a new sheet
        """
        # create the sheet
        # print("SheetMaker.__call__: building a new sheet instance")
        sheet = super().__call__(**kwds)

        # initialize the primary keys
        for accessor in self.pyre_primaries:
            # install the associated keymap
            sheet.pyre_keymaps[accessor] = accessor.keymap(sheet=sheet, column=accessor.index)
            # otherwise
        # and return it
        return sheet


# end of file 
