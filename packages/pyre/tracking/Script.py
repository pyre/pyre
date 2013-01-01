# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import os


# declaration
class Script:
    """
    A locator that records information relevant to python scripts. This information is
    typically extracted from stack traces so it contains whatever can be harvested by
    introspection
    """


    # meta methods
    def __init__(self, source, line=None, function=None):
        self.source = os.path.abspath(source)
        self.line = line
        self.function = function
        return


    def __str__(self):
        text = [
            "file={!r}".format(str(self.source))
            ]
        if self.line:
            text.append("line={.line!r}".format(self))
        if self.function:
            text.append("function={.function!r}".format(self))

        return ", ".join(text)


    # implementation details
    __slots__ = "source", "line", "function"


# end of file 
