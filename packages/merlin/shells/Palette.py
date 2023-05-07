# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# color table
class Palette:
    """
    The merlin color table
    """

    # metamethods
    def __init__(self, terminal, **kwds):
        # chain up
        super().__init__(**kwds)

        # colors
        self.normal = terminal.ansi["normal"]
        # generators
        self.project = terminal.x11["steel blue"]
        self.library = terminal.x11["steel blue"]
        # all done
        return


# end of file
