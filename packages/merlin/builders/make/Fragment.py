# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Generator import Generator


# the base makefile generator
class Fragment(Generator):
    """
    The base makefile fragment generator
    """

    # interface
    def generate(self, **kwds):
        """
        Generate the makefile preamble
        """
        # chain up
        super().generate(**kwds)
        # leave behind a marker in the main makefile
        yield self.renderer.commentLine(self.marker)
        # and construct the file include
        yield f"include {self.makefile.name}"
        # all done
        return


# end of file
