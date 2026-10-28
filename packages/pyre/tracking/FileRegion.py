# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a locator for a region of a file
class FileRegion:
    """
    A locator that records a region of a file, delimited by two file locators
    """

    # meta methods
    def __init__(self, start: object, end: object, **kwds) -> None:
        """
        Record the region from {start} to {end}, both positions within the same file
        """
        # chain up
        super().__init__(**kwds)
        # save the two ends of the region
        self.start = start
        self.end = end
        # all done
        return

    def __str__(self) -> str:
        """
        Render the file and whatever is known of the two ends of the region
        """
        # describe the start of the region
        start = self.position(locator=self.start)
        # and its end
        end = self.position(locator=self.end)
        # and put it all together; both ends are in the same file, so name it once
        return f"file={str(self.start.source)!r}, from ({start}) to ({end})"

    # implementation details
    def position(self, locator: object) -> str:
        """
        Render whatever is known of the position recorded by {locator}
        """
        # the known parts of the position
        text = []
        # if the line is known
        if locator.line is not None:
            # add it
            text.append(f"line={locator.line!r}")
        # if the column is known
        if locator.column is not None:
            # add it too
            text.append(f"column={locator.column!r}")
        # put it together
        return ", ".join(text)

    # my attributes
    __slots__ = "start", "end"


# end of file
