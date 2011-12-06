#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the merlin shell is accessible
"""


def test():
    # package access
    import os
    from merlin import merlin
    # mount the project directory
    project = merlin.vfs['/merlin/project']
    # check the project directory
    assert project.mountpoint == os.path.join(os.getcwd(), '.merlin')

    # debug: show me the vfs layout
    # merlin.vfs.dump()

    # and return
    return


# main
if __name__ == "__main__":
    test()


# end of file 
