#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the exceptions defined in the module are accessible
"""


def test():
    import pyre.db.pyrepg

    # make sure the exception object is accessible
    error = pyre.db.pyrepg.Error
    # make sure it is decorated correctly
    assert error.__name__ == 'Error'
    assert error.__module__ == 'pyrepg'
    assert error.__bases__ == (Exception,)
    # verify it can be caught
    try:
        raise pyre.db.pyrepg.Error
    except pyre.db.pyrepg.Error as error:
        pass

    return 


# main
if __name__ == "__main__":
    test()


# end of file 
