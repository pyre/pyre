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


import pyre.xml
from pyre.xml.Node import Node
from pyre.xml.Document import Document


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
    reader.read(stream=open("sample-schema.xml"), document=document)

    return


# main
if __name__ == "__main__":
    test()


# end of file 
