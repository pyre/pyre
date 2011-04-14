#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the merlin shell is accessible
"""


def test():
    # package access
    import os
    from merlin import merlin
    # mount the project directory
    project = merlin.mountProjectDirectory()
    # check the project directory
    assert project.mountpoint == os.path.join(os.getcwd(), '.merlin')
    # and return
    return


# main
if __name__ == "__main__":
    test()


# end of file 
