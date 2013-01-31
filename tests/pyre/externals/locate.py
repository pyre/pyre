#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    assert os.path.isdir(python.home)
    assert os.path.isdir(python.binaries)
    assert os.path.isdir(python.includes)
    assert os.path.isdir(python.libraryPath)
    assert os.path.isfile(python.executable)
    # show me
    # print('python: {}'.format(python))
    # print('  python: {.home}'.format(python))
    # print('  python: {.binaries}'.format(python))
    # print('  python: {.libraryPath}'.format(python))
    # print('  python: {.includes}'.format(python))
    # print('  executable: {.executable}'.format(python))

    # look for mpi; it's built-in so it must be there
    mpi = manager.locate(category='mpi')
    # check it
    assert mpi
    assert mpi.category == 'mpi'
    assert os.path.isdir(mpi.home)
    assert os.path.isdir(mpi.binaries)
    assert os.path.isdir(mpi.includes)
    assert os.path.isdir(mpi.libraryPath)
    assert os.path.isfile(mpi.launcher)
    # show me
    # print('mpi: {}'.format(mpi))
    # print('  home: {.home}'.format(mpi))
    # print('  bin: {.binaries}'.format(mpi))
    # print('  lib: {.libraryPath}'.format(mpi))
    # print('  inc: {.includes}'.format(mpi))
    # print('  launcher: {.launcher}'.format(mpi))

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
