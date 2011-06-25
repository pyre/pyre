#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise table declaration
"""


def test():
    # access to the package
    import pyre.db

    # declare a simple table
    class Weather(pyre.db.table, id="weather"):
        """
        The sample table from the postgre tutorial
        """

        # the fields
        city = pyre.db.str()
        city.doc = "the name of the city"

        date = pyre.db.date()
        date.doc = "the date of the measurement"


    # access to the journal
    import journal
    # quiet down the firewall we expect to breach
    journal.firewall("pyre.db").active = False

    # attempt to instantiate
    try:
        Weather()
        assert False
    except journal.FirewallError:
        pass

    # all done
    return Weather


# main
if __name__ == "__main__":
    test()


# end of file 
