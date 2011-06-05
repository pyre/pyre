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


    # meta methods
    def __init__(self, indenter=None, **kwds):
        super().__init__(**kwds)

        self._level = 0
        self._margin = ""
        self._indenter = self.INDENTER if indenter is None else indenter

        return


    # implementation details
    def _indent(self):
        """
        Increase the indentation level by one
        """
        self._level += 1
        self._margin = self._indenter * self._level
        return


    def _outdent(self):
        """
        Decrease the indentation level by one
        """
        self._level -= 1
        self._margin = self._indenter * self._level
        return


    def _render(self, line):
        return self._margin + line + "\n"


    # constants
    INDENTER = " "*4


    # private data
    _level = 0
    _margin = ""
    _indenter = None


# end of file 
