#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Build and test a simple tokenizer
"""

from pyre.parsing.Scanner import Scanner as BaseScanner


class Scanner(BaseScanner):
    """a simple scanner"""

    import pyre.parsing

    comment = pyre.parsing.token(r"#")
    separator = pyre.parsing.token(r":")
    delimiter = pyre.parsing.token(r",")
    terminator = pyre.parsing.token(r";")
    
    identifier = pyre.parsing.token(r"[_\w][_\wd]*")


def test():

    # open the input stream
    stream = open("sample.inp")

    # check
    actual = ()
    expected = ()
    assert expected == actual

    return


# main
if __name__ == "__main__":
    test()


# end of file 
