#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise python's understanding of the command line
"""


def test():
    import sys

    for index, arg in enumerate(sys.argv):
        print(index, arg, sep=": ")
    return


# main
if __name__ == "__main__":
    test()


# end of file
