#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that the merlin shell is accessible
"""


def test():
    # package access
    import os
    from merlin import merlin

    # debug:
    # merlin.vfs.dump()
    # merlin.nameserver.dump('merlin')
    
    # mount the project directory
    project = merlin.vfs['/merlin/project']
    # check the project directory
    assert project.uri == os.path.join(os.getcwd(), '.merlin')

    # and return
    return


# main
if __name__ == "__main__":
    test()


# end of file 
