#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Build a rudimentary data record
"""


import pyre.records


class record(pyre.records.dynamicrecord):
    """
    A sample record
    """


def test():
    return record


# main
if __name__ == "__main__":
    test()


# end of file 
