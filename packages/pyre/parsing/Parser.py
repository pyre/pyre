# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


class Parser:
    """
    The base class for parsers
    """


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # build my scanner
        self.scanner = self.lexer()
        # all done
        return


    # implementation details
    lexer = None # my scanner factory
    scanner = None # my scanner instance


# end of file 
