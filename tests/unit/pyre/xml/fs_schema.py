#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Build a document handler and read a simple file
"""


import pyre.xml
import pyre.filesystem
from pyre.xml.Node import Node
from pyre.xml.Document import Document


class File(Node):
    """Handle the file tag"""
    # storage for my attributes
    name = ""

    def notify(self, parent, locator):
        return parent.addEntry(self)

    def __init__(self, parent, attributes):
        self.name = attributes['name']
        self.fsnode = parent.fsnode.newNode()

    
class Folder(Node):
    """Handle the folder tag"""
    elements = ("file", "folder")

    def notify(self, parent, locator):
        return parent.addEntry(self)

    def addEntry(self, entry):
        """Add a file to my contents"""
        self.fsnode[entry.name] = entry.fsnode

    def __init__(self, parent, attributes):
        self.name = attributes['name']
        self.fsnode = parent.fsnode.newFolder()


class Filesystem(Folder):
    """The top level document element"""

    def notify(self, parent, locator):
        parent.dom = self.fsnode

    def __init__(self, parent, attributes):
        self.fsnode = pyre.filesystem.newVirtualFilesystem()


class FSD(Document):
    """Document class"""

    # the element descriptors
    file = pyre.xml.element(tag="file", handler=File)
    folder = pyre.xml.element(tag="folder", handler=Folder)
    filesystem = pyre.xml.element(tag="filesystem", handler=Filesystem)

    # the top-level
    elements = ["filesystem"]


def test():
    # build a parser
    reader = pyre.xml.newReader()
    # don't call my handlers on empty element content
    reader.ignoreWhitespace = True

    # parse the sample document
    fs = reader.read(stream=open("sample-fs-schema.xml"), document=FSD())

    # dump the contents
    fs._dump(False) # switch to True to see the contents

    # verify
    assert fs is not None
    assert fs["/"] is not None
    assert fs["/tmp"] is not None
    assert fs["/tmp/index.html"] is not None
    assert fs["/tmp/images"] is not None
    assert fs["/tmp/images/logo.png"] is not None

    return


# main
if __name__ == "__main__":
    test()


# end of file 
