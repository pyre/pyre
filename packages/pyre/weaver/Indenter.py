# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Indenter:
    """
    A mix-in class that keeps track of the indentation level
    """


    # interface
    def indent(self):
        """
        Increase the indentation level by one
        """
        self._level += 1
        self._margin = self._indenter * self._level
        return


    def outdent(self):
        """
        Decrease the indentation level by one
        """
        self._level -= 1
        self._margin = self._indenter * self._level
        return


    def place(self, line):
        return self._margin + line + "\n"


    # meta methods
    def __init__(self, indenter=None, **kwds):
        super().__init__(**kwds)

        self._level = 0
        self._margin = ""
        self._indenter = self.INDENTER if indenter is None else indenter

        return


    # constants
    INDENTER = " "*4


    # private data
    _level = 0
    _margin = ""
    _indenter = None


# end of file 
