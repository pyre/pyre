# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a locator for a position within a file
class File:
    """
    A locator that records a position within a file
    """

    # meta methods
    def __init__(
        self, source: object, line: int | None = None, column: int | None = None, **kwds
    ) -> None:
        """
        Record the {line} and {column} of a position within {source}
        """
        # chain up
        super().__init__(**kwds)
        # save the file
        self.source = source
        # and the position within it, either part of which may be unknown
        self.line = line
        self.column = column
        # all done
        return

    def __str__(self) -> str:
        """
        Render the file and whatever is known of the position within it
        """
        # start with the file
        text = [f"file={str(self.source)!r}"]
        # if the line is known
        if self.line is not None:
            # add it
            text.append(f"line={self.line!r}")
        # if the column is known
        if self.column is not None:
            # add it too
            text.append(f"column={self.column!r}")
        # put it all together
        return ", ".join(text)

    # implementation details
    __slots__ = "source", "line", "column"


# end of file
