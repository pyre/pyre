# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from ... import descriptors


# declaration
class FieldReference(descriptors.stem.variable):
    """
    A field decorator that encapsulates references to table fields

    This class is endowed with the full algebra from {pyre.algebraic} in order to support
    expressions involving table fields. Such expressions can be used to formulate constraints
    or to specify fields in views
    """

    # public data
    table = None  # the table class
    field = None  # the field descriptor

    # interface
    def coerce(self, **kwds):
        """
        Convert {value} into my type
        """
        # get my field to do this
        return self.field.coerce(**kwds)

    def project(self, table):
        """
        Build a reference to the given {table} that points to the same field as i do
        """
        # easy enough
        return type(self)(table=table, field=self.field)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a reference to a field
        """
        # ask for my handler
        return authority._pyre_onFieldReference(node=self, **kwds)

    # meta-methods
    def __init__(self, table, field, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my referents
        self.table = table
        self.field = field
        # all done
        return


# end of file
