# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# declaration
class Script:
    """
    A locator that records information relevant to python scripts. This information is
    typically extracted from stack traces so it contains whatever can be harvested by
    introspection
    """


    # metamethods
    def __init__(self, source, line=None, function=None):
        # save my info
        self.source = source
        self.line = line
        self.function = function
        # all done
        return


    def __str__(self):
        # initialize with the file name
        text = [ f"file='{self.source}'"]
        # if we know the line number
        if self.line:
            # add it to the pile
            text.append(f"line={self.line}")
        # if we know the function name
        if self.function:
            # add it to the pile
            text.append(f"function='{self.function}'")
        # assemble and return
        return ", ".join(text)


    # implementation details
    __slots__ = "source", "line", "function"


# end of file
