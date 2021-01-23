# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# declaration
class FileRegion:
    """
    A locator that records information about a region of a file
    """


    # metamethods
    def __init__(self, start, end):
        # record the start and end locators of the file region
        self.start = start
        self.end = end
        # all done
        return


    def __str__(self):
        # prime
        start = []
        # if the start locator has a line number
        if self.start.line:
            # add it to the pile
            start.append(f"line={self.start.line}")
        # if it has a column number
        if self.start.column:
            # add it to the pile
            start.append(f"column={self.start.column}")
        # assemble the start specification
        start = ", ".join(start)

        # end of the region
        end = []
        # if the end locator has a line number
        if self.end.line:
            # add it to the pile
            end.append(f"line={self.end.line}")
        # if it knows the column number
        if self.end.column:
            # add it to the pile
            end.append(f"column={self.end.column}")
        # assemble the end specification
        end = ", ".join(end)

        # put it all together
        text = f"file='{self.start.source}', from ({start}) to ({end})"

        # all done
        return text


    # implementation details
    __slots__ = "start", "end"


# end of file
