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
    def generate(self, makefile, marker, **kwds):
        """
        Generate the makefile preamble
        """
        # chain up
        super().generate(makefile=makefile, **kwds)
        # leave behind a marker in the main makefile
        yield self.renderer.commentLine(marker)
        # and construct the file include
        yield f"include merlin/{makefile.name}"
        # all done
        return


# end of file
