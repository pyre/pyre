# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .Fragment import Fragment


# the preamble with the makefile boilerplate
class Compilers(Fragment):
    """
    The generator of the makefile with the compiler support
    """

    # configurable state
    makefile = merlin.properties.path()
    makefile.default = "compilers"
    makefile.doc = "the generated makefile"

    # interface
    def generate(self, stage, **kwds):
        """
        Generate my makefile
        """
        # build the makefile path
        makefile = stage / "merlin" / self.makefile
        # and a comment
        marker = f"compiler settings"
        # chain up
        yield from super().generate(makefile=makefile, marker=marker, **kwds)

    # implementation details
    def _generate(self, plexus, builder, target="projects", **kwds):
        """
        Build my contents
        """
        # chain up
        yield from super()._generate(builder=builder, **kwds)
        # get the table of compilers
        compilers = plexus.compilers
        # get my renderer
        renderer = self.renderer

        # go through the selected compilers
        for compiler in compilers:
            # and ask the builder to get each one to generate a section with its settings
            yield from builder.identify(visitor=compiler, plexus=plexus, **kwds)

        # all done
        return


# end of file
