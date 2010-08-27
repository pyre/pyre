# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Script:
    """
    Locator that records information relevant to python scripts. This information is typically
    extracted from stack traces so it contains whatever can be harvested by introspection
    """


    # public data
    source = None
    line = None
    function = None


    # meta methods
    def __init__(self, source, line, function, **kwds):
        super().__init__(**kwds)

        self.source = source
        self.line = line
        self.function = function

        return


    def __str__(self):
        text = [
            "file={0.source!r}".format(self)
            ]
        if self.line:
            text.append("line={0.line!r}".format(self))
        if self.function:
            text.append("function={0.function!r}".format(self))

        return ", ".join(text)


# end of file 
