#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Build and test a simple tokenizer
"""

from pyre.parsing.Scanner import Scanner


class Simple(Scanner):
    """a simple scanner"""

    # tokens
    comment = Scanner.token(r"#.*$")
    separator = Scanner.token(r":")
    delimiter = Scanner.token(r",")
    terminator = Scanner.token(r";")
    
    identifier = Scanner.token(r"[_\w]+")

    # constants
    ignoreWhitespace = True


def test():

    filename = "sample-bad.inp"
    # open the input stream
    stream = open(filename)
    # create a scanner
    scanner = Simple()

    # tokenize
    try:
        list(scanner.tokenize(stream))
        assert False
    except scanner.TokenizationError as error:
        assert error.locator.source == filename
        assert error.locator.line == 6
        assert error.locator.column == 31

    return


# main
if __name__ == "__main__":
    test()


# end of file 
