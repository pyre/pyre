#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

"""
Read an empty document
"""


import xml
import pyre.xml
from pyre.xml.Node import Node as BaseNode
from pyre.xml.Document import Document


class Node(BaseNode):
    """Base class for node handlers of this document"""

    namespace = "http://pyre.caltech.edu/releases/1.0/schema/inventory.html"


class Inventory(Node):
    """The top level document element"""

    def notify(self, parent, locator):
        """do nothing"""

    def __init__(self, parent, attributes, locator):
        """do nothing"""


class IDoc(Document):
    """Document class"""
    # the top-level
    root = "inventory"
    # declare the handler
    inventory = pyre.xml.element(tag="inventory", handler=Inventory)


def test():
    # build the trivial document
    document = IDoc()

    # build a parser
    reader = pyre.xml.newReader()
    # parse the sample document
    reader.read(
        stream=open("sample-namespaces.xml"), 
        document=document,
        features=[(reader.feature_namespaces, True)]
        )

    return document


# main
if __name__ == "__main__":
    test()


# end of file 
