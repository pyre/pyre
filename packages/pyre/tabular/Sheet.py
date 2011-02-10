# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import itertools
from .Templater import Templater


class Sheet(metaclass=Templater):
    """
    The base class for worksheets
    """


    # types
    from .Index import Index as pyre_indexedAccessor
    from .Column import Column as pyre_measureAccessor


    # public data
    pyre_name = None # the name of the sheet
    pyre_data = None # the list of records
    pyre_primaries = None # a list of measure accessors that are primary keys
    pyre_keymaps = None # storage for measures that are primary keys

    pyre_items = () # the full set of measures and derivations
    pyre_localItems = () # the locally declared measures and derivations


    # interface
    def populate(self, data):
        """
        Assume that the layout of the iterable {data} is compatible with my record layout; use
        it to populate my data set

        Compatibility with my record layout implies that {data} is a container of records, and
        each record is itself an iterable that has as many entries as i have measures.
        """
        # iterate of the reords in {data}
        for datum in data:
            # populate the data set
            self.append(record=self.pyre_Record(datum))
        # all done
        return self
                        
        
    def append(self, record):
        """
        Add {record} to my data set
        """
        # the collation number of this record
        rank = len(self.pyre_data)
        # update my indices
        for primary in self.pyre_primaries:
            # grab the associated keymap
            keymap = self.pyre_keymaps[primary]
            # the key is the value of the indexed column
            key = record[primary.index]
            # update
            keymap[key] = rank
        # what's the right thing to do when a new record with a key conflict shows up?
        # add the record to the data set
        self.pyre_data.append(record)
        # return 
        return self
        

    # introspection
    @classmethod
    def pyre_offset(cls, measure):
        """
        Return the offset of {measure} within my records
        """
        return cls.__dict__[measure.name].index


    # meta methods
    def __init__(self, name=None, **kwds):
        super().__init__(**kwds)

        self.pyre_name = name
        self.pyre_data = []
        self.pyre_keymaps = {} # populated by my metaclass

        return


    def __getitem__(self, index):
        """
        Indexed access to the data
        """
        # delegate to the storage
        return self.pyre_data[index]


    def __len__(self):
        """
        Compute the number of records in the sheet
        """
        return len(self.pyre_data)


    def __iter__(self):
        """
        Build an iterator over my data set
        """
        return iter(self.pyre_data)


# end of file 
