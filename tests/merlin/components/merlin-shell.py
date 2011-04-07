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
    import merlin
    # invoke its main entry point
    executive = merlin.boot()
    # check the project directory
    assert executive.project.mountpoint == os.path.join(os.getcwd(), '.merlin')
    # and return
    return


# main
if __name__ == "__main__":
    test()


# end of file 
