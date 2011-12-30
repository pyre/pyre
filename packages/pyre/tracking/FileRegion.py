# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class FileRegion:
    """
    Locator that records information about a region of a file
    """


    # public data
    start = None
    end = None


    # meta methods
    def __init__(self, start, end, **kwds):
        super().__init__(**kwds)

        self.start = start
        self.end = end

        return


    def __str__(self):
        # start of the region
        start = []
        if self.start.line:
            start.append("line={0.line!r}".format(self.start))
        if self.start.column:
            start.append("column={0.column!r}".format(self.start))
        start = ", ".join(start)

        # end of the region
        end = []
        if self.end.line:
            end.append("line={0.line!r}".format(self.end))
        if self.end.column:
            end.append("column={0.column!r}".format(self.end))
        end = ", ".join(end)

        text = "file={0!r}, from ({1}) to ({2})".format(self.start.source, start, end)

        return text


# end of file 
