#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""

def test():

    from pyre.units.exceptions import (
        UnitError
        )

    try:
        raise UnitError(msg=None)
    except UnitError as error:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
