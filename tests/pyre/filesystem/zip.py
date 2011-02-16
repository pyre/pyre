#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify creation of filesystems based on zipfiles
"""


def test():
    import os
    import zipfile
    import pyre.filesystem


    # the name of the zipfile
    archive = "/tmp/sample.zip"
    # build the archive
    target = zipfile.ZipFile(file=archive, mode="w")
    for filename in os.listdir('.'):
        target.write(filename)
    target.close()
    
    # open it as a filesystem
    home = pyre.filesystem.newZipFilesystem(root=archive)
    home.dump(interactive=False) # change to True to see the dump

    # remove the zipfile
    os.unlink(archive)

    return home


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.filesystem" }

    test()

    # destroy pyre.fileserver so it doesn't confuse the extent
    import pyre
    pyre.shutdown()

    # check that the filesystem was destroyed
    from pyre.filesystem.Filesystem import Filesystem
    # print("Filesystem extent:", len(Filesystem._pyre_extent))
    assert len(Filesystem._pyre_extent) == 0

    # now check that the nodes were all destroyed
    from pyre.filesystem.Node import Node
    # print("Node extent:", len(Node._pyre_extent))
    assert len(Node._pyre_extent) == 0


# end of file 
