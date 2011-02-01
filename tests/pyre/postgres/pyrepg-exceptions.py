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
    import pyre.postgres.pyrepg
    from pyre.framework.exceptions import FrameworkError

    # make sure the exception object is accessible
    error = pyre.postgres.pyrepg.Error
    # make sure it is decorated correctly
    assert error.__name__ == 'Error'
    assert error.__module__ == 'pyre.db.exceptions'
    assert error.__bases__ == (FrameworkError,)
    # verify it can be caught
    try:
        raise pyre.postgres.pyrepg.Error('a generic database error')
    except pyre.postgres.pyrepg.Error as error:
        pass

    return 


# main
if __name__ == "__main__":
    test()


# end of file 
