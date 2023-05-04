#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Exercise the URI parser
"""


def test():
    import pyre.schemata

    # make a converter
    ostream = pyre.schemata.ostream()

    # open a file that exists
    f = ostream.coerce('file:output.cfg')
    assert f.name == 'output.cfg'

    # anything else?
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
