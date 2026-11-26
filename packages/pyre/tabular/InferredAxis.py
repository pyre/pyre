# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class InferredAxis(dict):
    """
    The map from each distinct value of the measure of an inferred dimension to the set of rows
    of the sheet of a chart that hold it
    """

    # meta-methods
    def __init__(self, chart, dimension, **kwds):
        """
        Collect the rows of the sheet of {chart} by the value of the measure of {dimension}
        """
        # chain up
        super().__init__(**kwds)

        # get the sheet
        sheet = chart.sheet
        # the measure
        measure = dimension.measure
        # and my column number
        column = sheet.pyre_columns[measure]

        # go through the records
        for row, record in enumerate(sheet.pyre_data):
            # get the value of my measure
            value = record[column]
            # get the set of rows that have the same value
            rows = self.setdefault(value, set())
            # and add this one to it
            rows.add(row)

        # all done
        return


# end of file
