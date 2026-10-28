# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a locator for a place in python code
class Script:
    """
    A locator that records a place in python code: the file, the line, and the function
    """

    # meta methods
    def __init__(
        self, source: object, line: int | None = None, function: str | None = None, **kwds
    ) -> None:
        """
        Record the {line} of {source} and the {function} it belongs to
        """
        # chain up
        super().__init__(**kwds)
        # save the file
        self.source = source
        # the line, which may be unknown
        self.line = line
        # and the function, which may be unknown as well
        self.function = function
        # all done
        return

    def __str__(self) -> str:
        """
        Render the file and whatever is known of the place within it
        """
        # start with the file
        text = [f"file={str(self.source)!r}"]
        # if the line is known
        if self.line is not None:
            # add it
            text.append(f"line={self.line!r}")
        # if the function is known
        if self.function is not None:
            # add it too
            text.append(f"function={self.function!r}")
        # put it all together
        return ", ".join(text)

    # implementation details
    __slots__ = "source", "line", "function"


# end of file
