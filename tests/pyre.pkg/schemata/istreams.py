#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2022 all rights reserved
#


"""
Exercise the URI parser
"""


def test():
    import pyre.schemata

    # make a converter
    istream = pyre.schemata.istream()

    # open a file that exists
    f = istream.coerce('file:istreams.py')
    assert f.name == 'istreams.py'

    # a poorly formed one
    bad = "&"
    try:
        istream.coerce(bad)
        assert False
    except istream.CastingError as error:
        assert str(error) == f"could not coerce '{bad}' into a URI"

    # anything else?
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
