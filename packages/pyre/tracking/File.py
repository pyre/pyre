# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class File(object):
    """
    Locator that records information relevant to file sources
    """


    # public data
    source = None
    line = None
    column = None


    # meta methods
    def __init__(self, source, line, column, **kwds):
        super().__init__(**kwds)

        self.source = source
        self.line = line
        self.column = column

        return


    def __str__(self):
        text = [
            "file={0.source!r}".format(self)
            ]
        if self.line is not None:
            text.append("line={0.line!r}".format(self))
        if self.column is not None:
            text.append("column={0.column!r}".format(self))

        return ", ".join(text)


# end of file 
