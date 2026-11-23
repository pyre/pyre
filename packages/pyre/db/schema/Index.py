# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my declaration
class Index:
    """
    An index over some of the fields of a table, possibly unique, possibly over only the rows
    that pass a predicate
    """

    # interface
    def identifier(self, table):
        """
        Build my name as an index of {table}: the one i was given, or one made of the name of
        {table} and those of my fields
        """
        # an index with a name of its own
        if self.name is not None:
            # goes by it
            return self.name
        # the rest are named after the table and their fields
        return "_".join([table.pyre_name, *(field.name for field in self.fields), "index"])

    # meta-methods
    def __init__(self, fields, unique=False, where=None, name=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the fields i cover, in order
        self.fields = fields
        # whether no two rows may share their values
        self.unique = unique
        # the predicate a row must pass to be covered; {None} covers them all
        self.where = where
        # my name; {None} for the one made of the names of my table and my fields
        self.name = name
        # all done
        return


# end of file
