#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the module is accessible
"""


def test():
    import pyre.db.pyrepg

    try:
        raise pyre.db.pyrepg.Error
    except pyre.db.pyrepg.Error as error:
        pass

    return 


# main
if __name__ == "__main__":
    test()


# end of file 
