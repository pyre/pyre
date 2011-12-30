# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from .. import records

class CSV:
    """
    A reader/writer of sheets in csv format

    This class leverages {pyre.records.CSV} to read/write sheet records
    """


    # public data
    csv = records.csv()


    # interface
    def read(self, sheet, **kwds):
        """
        Given a {sheet} instance, populate it by reading records from a data source.

        The {kwds} arguments are passed straight through to {pyre.records.CSV}, which is
        responsible for the actual opening of the input stream and the creation of the sheet
        data records. The current implementation supports either the specification of an actual
        data {stream}, an open file-like object, or a {uri}, in which case the reader will
        attempt to create the stream object itself. See {pyre.records.CSV} for the exact
        details.
        """
        # prime the record generator and start reading data
        sheet.pyre_populate(data=self.csv.read(layout=sheet.pyre_Record, **kwds))
        # and return the sheet
        return sheet
        

    # exceptions
    from ..records.exceptions import SourceSpecificationError


# end of file 
