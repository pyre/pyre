#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the unit parser works as advertised
"""


def test():
    import pyre.units
    parser = pyre.units.parser()

    import pyre.units.SI as SI

    assert SI.kilogram == parser.parse("kilogram")
    assert SI.meter == parser.parse("meter")
    assert SI.second == parser.parse("second")
    assert SI.ampere == parser.parse("ampere")
    assert SI.mole == parser.parse("mole")
    assert SI.candela == parser.parse("candela")

    return


# main
if __name__ == "__main__":
    test()


# end of file 
