#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Read a blank file
"""


def test():
    import xml.sax
    import pyre.xml

    # create a trivial document
    from pyre.xml.Document import Document
    document = Document()

    # build a parser
    reader = pyre.xml.newReader()
    # parse the sample document
    try:
        reader.read(stream=open("sample-blank.xml"), document=document)
        assert False
    except reader.ParsingError as error:
        assert str(error) == "file='sample-blank.xml', line=11, column=0: no element found"

    return document


# main
if __name__ == "__main__":
    test()


# end of file 
