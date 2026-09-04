# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# content accumulator
class Entry:
    """
    Accumulator of content and metadata for journal messages
    """

    # public data
    page = None  # a list of lines of output
    notes = None  # a dictionary with the message metadata

    # metamethods
    def __init__(self, notes, page=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # start with a copy of the supplied page, or a blank one
        self.page = list(page) if page is not None else []
        # and a copy of the supplied metadata
        self.notes = dict(notes)
        # all done
        return

    def __iter__(self):
        """
        Support for quick unpacking
        """
        # first the page
        yield self.page
        # then the notes
        yield self.notes
        # all done
        return


# end of file
