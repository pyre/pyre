#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Reject a value just below the start of an interval
"""


def test():
    """
    Bin values over an interval, and check that one just below its start is rejected instead of
    landing in the first bin, while the start itself and a value just inside the end are binned
    """
    # get the package
    import pyre.tabular

    # a sheet
    class sales(pyre.tabular.sheet):
        """
        The transaction data
        """

        # the amount of each sale
        quantity = pyre.tabular.float()

    # a chart
    class chart(pyre.tabular.chart, sheet=sales):
        """
        Categorize the sales by quantity
        """

        # in two bins over (0, 10)
        quantity = pyre.tabular.interval(measure=sales.quantity, interval=(0, 10), subdivisions=2)

    # the data: just below the start, the start, and just inside the end
    data = [(-0.5,), (0.0,), (9.5,)]
    # make a sheet
    transactions = sales(name="sales").pyre_immutable(data)
    # and chart it
    cube = chart(sheet=transactions)
    # get the axis
    quantities = cube.quantity

    # check that the value below the start was rejected
    assert quantities.rejects == [0], quantities.rejects
    # that the start went to the first bin
    assert quantities[0] == {1}, quantities[0]
    # and the value just inside the end to the last
    assert quantities[1] == {2}, quantities[1]

    # all done
    return cube


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
