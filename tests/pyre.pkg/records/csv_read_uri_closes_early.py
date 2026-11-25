#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the csv reader closes the file it opens when its client stops reading early
"""


def test():
    """
    Read the first record of a csv file named by its uri, stop, and check that the reader leaves
    no file open behind it
    """
    # externals
    import gc
    import warnings

    # access the package
    import pyre.records

    # a record
    class item(pyre.records.record):
        """
        The stock keeping unit and description of an item
        """

        # the stock keeping unit
        sku = pyre.records.str()
        # and the description
        description = pyre.records.str()

    # make a reader
    csv = pyre.records.csv()
    # watch for the warning python issues when it collects a file that is still open
    with warnings.catch_warnings(record=True) as caught:
        # by recording every one of them
        warnings.simplefilter("always", ResourceWarning)
        # start reading
        records = csv.immutable(layout=item, uri="vegetables.csv")
        # get the first record
        first = next(records)
        # stop reading
        records.close()
        # and collect what is left of the reader
        gc.collect()

    # check that the first record was read
    assert tuple(first) == ("4000", "tomatoes"), tuple(first)
    # and that nothing was left open
    leaks = [warning for warning in caught if issubclass(warning.category, ResourceWarning)]
    # by finding no warnings about it
    assert not leaks, [str(leak.message) for leak in leaks]

    # all done
    return first


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
