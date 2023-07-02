# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .Fragment import Fragment


# the makefile fragment with the compiler settings
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
    def _generate(self, plexus, builder, **kwds):
        """
        Build my contents
        """
        # chain up
        yield from super()._generate(builder=builder, **kwds)
        # get the renderer
        renderer = builder.renderer
        # ask {merlin} for the table of compilers
        compilers = plexus.compilers
        # go through the selected compilers
        for compiler in compilers:
            # get the language
            language = compiler.language
            # assemble my version
            version = ".".join(compiler.version)
            # mark
            yield renderer.commentLine(f"{language} compiler support")
            # my driver
            yield from renderer.set(
                name=f"{language}.driver", value=f"{compiler.driver}"
            )
            # its version
            yield from renderer.set(name=f"{language}.version", value=f"{version}")
            # leave some room
            yield ""

            # the compile command line
            yield renderer.commentLine(f"usage: {language}.compile <source> <object>")
            # generate
            yield from renderer.setq(
                name=f"{language}.compile",
                multi=compiler.compile(
                    builder=builder,
                    driver=f"$({language}.driver)",
                    source="$(1)",
                    object="$(2)",
                    **kwds,
                ),
            )
            # leave some room
            yield ""

            # the link command line
            yield renderer.commentLine(f"usage: {language}.link <source> <object>")
            # generate
            yield from renderer.setq(
                name=f"{language}.link",
                multi=[
                    f"$({language}.driver)",
                ],
            )
            # leave some room
            yield ""

        # all done
        return


# end of file
