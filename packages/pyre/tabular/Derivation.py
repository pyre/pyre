# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..records.Derivation import Derivation as RecordDerivation


class Derivation(RecordDerivation):
    """
    The base class for table descriptors
    """


    # public data in addition to what is inherited from records.Derivation
    index = False # NYI; should never be True for derivations


    # interface
    def pyre_sheetColumnAccessor(self, sheet, index):
        """
        Ask the {sheet} for an accessor factory that is appropriate for measures, and use it to
        build an accessor that knows my index in the tuple of items
        """
        # otherwise, ask for and return an accessor
        return sheet.pyre_measureAccessor(index=index, measure=self)
        


# end of file 
