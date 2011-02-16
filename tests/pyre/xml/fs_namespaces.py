#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Build a document handler and read a simple file
"""


import xml
import pyre.xml
import pyre.filesystem
from pyre.xml.Node import Node as BaseNode
from pyre.xml.Document import Document


class Node(BaseNode):
    """Base class for my nodes"""
    namespace = "http://pyre.caltech.edu/releases/1.0/schema/fs.html"


class File(Node):
    """Handle the file tag"""

    def notify(self, parent, locator):
        return parent.addEntry(self)

    def __init__(self, parent, attributes, locator):
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

    def __init__(self, parent, attributes, locator):
        self.name = attributes['name']
        self.fsnode = parent.fsnode.newFolder()


class Filesystem(Folder):
    """The top level document element"""

    def notify(self, parent, locator):
        parent.dom = self.fsnode

    def __init__(self, parent, attributes, locator):
        self.fsnode = pyre.filesystem.newVirtualFilesystem()


class FSD(Document):
    """Document class"""

    # the top-level
    root = "filesystem"

    # the element descriptors
    file = pyre.xml.element(tag="file", handler=File)
    folder = pyre.xml.element(tag="folder", handler=Folder)
    filesystem = pyre.xml.element(tag="filesystem", handler=Filesystem)


def test():
    # build a parser
    reader = pyre.xml.newReader()
    # don't call my handlers on empty element content
    reader.ignoreWhitespace = True

    # parse the sample document
    fs = reader.read(
        stream=open("sample-fs-namespaces.xml"),
        document=FSD(),
        features=[(reader.feature_namespaces, True)]
        )

    # dump the contents
    fs.dump(False) # switch to True to see the contents

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
