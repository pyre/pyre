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

    # build a parser
    reader = pyre.xml.newReader()
    # parse the sample document
    try:
        reader.read(stream=open("blank.xml"), document=None)
        assert False
    except reader.ParsingError as error:
        assert str(error) == "file='blank.xml', line=11: no element found"

    return


# main
if __name__ == "__main__":
    test()


# end of file 
