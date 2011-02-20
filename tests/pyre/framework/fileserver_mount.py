#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercises the fileserver
"""


def test():
    import pyre.framework
    import pyre.filesystem
    # build the executive
    executive = pyre.framework.executive()
    # access the fileserver
    fs = executive.fileserver

    # build a file system for the current directory
    local = pyre.filesystem.newLocalFilesystem('.').discover()
    # and mount it
    fs['local'] = local
    # check that this file is there
    assert fs['local/fileserver_mount.py']
    # dump the filesystem
    fs.dump(False) # switch to True to see the dump

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
