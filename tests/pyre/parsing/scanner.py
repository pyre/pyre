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

def test():
    from pyre.parsing.Scanner import Scanner

    COMMENT = r"#"
    SEPARATOR = r":"

    class Simple(Scanner):
        """a simple scanner"""
        comment = Scanner.token(COMMENT)
        separator = Scanner.token(SEPARATOR)


    # access the token base class
    from pyre.parsing.Token import Token

    # check that the token descriptors have been turned into subclasses of Token
    assert issubclass(Simple.comment, Token)
    assert issubclass(Simple.separator, Token)
    # check that the token index reflects the transmutation
    assert getattr(Simple, Simple.pyre_TOKEN_INDEX) == [Simple.comment, Simple.separator]
    # check that the recognizer was built correctly
    assert Simple.recognizer.pattern == "(?P<comment>#)|(?P<separator>:)"
    
    # and return the class record
    return Simple


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
