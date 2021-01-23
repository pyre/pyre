# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# declaration
class File:
    """
    A locator that records a position within a file
    """


    # metamethods
    def __init__(self, source, line=None, column=None):
        # save my info
        self.source = source
        self.line = line
        self.column = column
        # all done
        return


    def __str__(self):
        # prime the message with the file name
        text = [ f"file='{self.source}'" ]
        # if we know the line number
        if self.line is not None:
            # add it on
            text.append(f"line={self.line}")
        # if we know the column number
        if self.column is not None:
            # add it on
            text.append(f"column={self.column}")
        # assemble and return
        return ", ".join(text)


    # implementation details
    __slots__ = "source", "line", "column"


# end of file
