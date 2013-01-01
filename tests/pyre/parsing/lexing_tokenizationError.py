#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Build and test a simple tokenizer
"""

def test():
    import pyre.parsing


    class Simple(pyre.parsing.scanner):
        """a simple scanner"""

        # tokens
        comment = pyre.parsing.token(r"#.*$")
        separator = pyre.parsing.token(r":")
        delimiter = pyre.parsing.token(r",")
        terminator = pyre.parsing.token(r";")

        identifier = pyre.parsing.token(r"[_\w]+")


    filename = "sample-bad.inp"
    # open the input stream
    stream = open(filename)
    # create a scanner
    scanner = Simple()

    # tokenize
    try:
        list(scanner.pyre_tokenize(uri=filename, stream=stream))
        assert False
    except scanner.TokenizationError as error:
        assert error.locator.source == filename
        assert error.locator.line == 7
        assert error.locator.column == 31

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
