#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Verify that the file server can mount arbitrary locations 
"""


def test():
    import pyre.framework
    # build the executive
    executive = pyre.framework.executive()
    # access the file server
    fs = executive.fileserver

    # build a file system for the current directory
    local = fs.local(root='.').discover(levels=1)
    # and mount it
    fs['cwd'] = local
    # check that this file is there
    assert fs['cwd/fileserver_mount.py']
    # dump the filesystem
    fs.dump(False) # switch to True to see the dump

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
