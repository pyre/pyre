#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Ask the manager for a package based only on its category
"""


def test():
    # externals
    import os
    # get the framework
    import pyre
    # get the registered package manager
    manager = pyre.executive.externals

    # look for python; it's built-in so it must be there
    python = manager.locate(category='python')
    # check it
    assert python
    assert python.category == 'python'
    # show me
    print('python: {.pyre_spec}'.format(python))
    print('  path: {.path}'.format(python))
    print('  ldpath: {.ldpath}'.format(python))
    print('  include: {.include}'.format(python))
    print('  interpreter: {.interpreter}'.format(python))

    # attempt to
    try:
        # look for something that shouldn't exist
        manager.locate(category='<unsupported>')
        # verify that an exception was raised
        assert False
    # catch the right exception
    except manager.ExternalNotFoundError as error:
        # verify that the error message captured the category name
        assert error.category == '<unsupported>'

    # all done
    return manager


# main
if __name__ == "__main__":
    # do...
    test()


# end of file 
