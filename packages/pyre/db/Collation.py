# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


class Collation:
    """
    An encapsulation of the collation sequence
    """

    # types
    from .FieldReference import FieldReference as fieldReference

    # public data
    fieldref = None  # the reference to the field whose values are sorted
    collation = "ASC"  # and the order of the sort

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a collation
        """
        # ask for my handler
        return authority._pyre_onCollation(node=self, **kwds)

    # meta methods
    def __init__(self, fieldref, collation=collation, **kwds):
        # chain up
        super().__init__(**kwds)

        # if necessary
        if not isinstance(fieldref, self.fieldReference):
            # convert field to references
            fieldref = self.fieldReference(field=fieldref, table=None)

        # save the field reference and the collation order
        self.fieldref = fieldref
        self.collation = collation

        # all done
        return


# end of file
