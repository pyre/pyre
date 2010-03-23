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

    # open the input stream
    stream = open("sample.inp")
    # create a scanner
    scanner = Simple()

    # tokenize
    actual = list(scanner.tokenize(stream))

    # check
    expected = (
        Simple.start,
        Simple.comment, Simple.comment, Simple.comment, Simple.comment, Simple.comment,
        Simple.identifier, Simple.separator, 
        Simple.identifier, Simple.delimiter,
        Simple.identifier, Simple.delimiter,
        Simple.identifier,
        Simple.terminator,
        Simple.comment,
        Simple.finish,
        )

    for token, klass in zip(actual, expected):
        assert isinstance(token, klass)

    return


# main
if __name__ == "__main__":
    test()


# end of file 
