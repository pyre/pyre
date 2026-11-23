# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# color table
class Palette:
    """
    The merlin color table
    """

    # metamethods
    def __init__(self, terminal, **kwds):
        # chain up
        super().__init__(**kwds)

        # colors: the plain one, which ends any other
        self.normal = terminal.reset()
        # generators: projects
        self.project = terminal.color("steel blue")
        # and libraries
        self.library = terminal.color("steel blue")
        # all done
        return


# end of file
