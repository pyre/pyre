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

    from pyre.schema.exceptions import (
        SchemaError, CastingError
        )

    try:
        raise SchemaError(msg=None)
    except SchemaError as error:
        pass

    try:
        raise CastingError(msg=None, value=None)
    except CastingError as error:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
