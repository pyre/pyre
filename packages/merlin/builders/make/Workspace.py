# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .Fragment import Fragment


# the preamble with the makefile boilerplate
class Workspace(Fragment):
    """
    The generator of the makefile with the boilerplate support
    """

    # configurable state
    makefile = merlin.properties.path()
    makefile.default = "ws"
    makefile.doc = "the generated makefile"

    # interface
    def generate(self, stage, **kwds):
        """
        Generate my makefile
        """
        # build the makefile path
        makefile = stage / "merlin" / self.makefile
        # and a comment
        marker = f"workspace information"
        # chain up
        yield from super().generate(makefile=makefile, marker=marker, **kwds)

    # implementation details
    def _generate(self, plexus, builder, **kwds):
        """
        Build my contents
        """
        # chain up
        yield from super()._generate(builder=builder, **kwds)
        # get the source control system
        scs = plexus.scs
        # get my renderer
        renderer = self.renderer

        # ask the source control system to generate the fragment that extracts the
        # repository revision information
        # yield from scs.make(renderer=renderer)
        yield from builder.identify(visitor=scs, plexus=plexus, **kwds)

        # add the path to the file with the live workspace revision information
        yield renderer.commentLine("the live workspace info")
        # save the value
        yield from renderer.set(name="ws.rev.now", value=f"$(build)/ws.rev.now")
        # and the path to the file with the archived workspace revision information
        yield renderer.commentLine("the archived workspace info")
        # save the value
        yield from renderer.set(name="ws.rev", value=f"$(build)/ws.rev")
        # make some room
        yield ""

        # target for the file with the current workspace revision information
        yield renderer.commentLine(f"make the file with the live revision information")
        # build the target
        yield f"ws.rev.now: | $(build)"
        # log
        yield f"\t@$(call log.action,{plexus.scs.name},$(ws.tag))"
        # the rule
        yield f"\t@$(echo) '# -*- Makefile -*-' > $(ws.rev.now)"
        yield f"\t@$(echo) ' ' >> $(ws.rev.now)"
        yield f"\t@$(echo) '# repository info' >> $(ws.rev.now)"
        yield f"\t@$(echo) ' ' >> $(ws.rev.now)"
        yield f"\t@$(echo) ws.tag := $(ws.tag) >> $(ws.rev.now)"
        yield f"\t@$(echo) ws.major := $(ws.major) >> $(ws.rev.now)"
        yield f"\t@$(echo) ws.minor := $(ws.minor) >> $(ws.rev.now)"
        yield f"\t@$(echo) ws.micro := $(ws.micro) >> $(ws.rev.now)"
        yield f"\t@$(echo) ws.revision := $(ws.revision) >> $(ws.rev.now)"
        yield f"\t@$(echo) ws.date := $(shell $(date.date)) >> $(ws.rev.now)"
        yield f"\t@$(echo) ' ' >> $(ws.rev.now)"
        yield f"\t@$(echo) '# end of file' >> $(ws.rev.now)"
        # make some room
        yield ""

        # target for the file with the archive workspace revision information
        yield renderer.commentLine(f"the file with the archived revision information")
        # build the target
        yield f"$(ws.rev): ws.rev.now"
        # the rule
        yield f"\t@if ! $(diff) $(ws.rev.now) $(ws.rev) >& /dev/null; then \\"
        yield f"      $(call log.action,rev,/stage/build/ws.rev) ; \\"
        yield f"      $(cp) $(ws.rev.now) $(ws.rev) ; \\"
        yield f"    fi"
        # make some room
        yield ""

        # load the file with the repository information
        yield renderer.commentLine(f"load the repository information")
        # add the instruction
        yield "projects:: $(ws.rev)"
        # make some room
        yield ""

        # all done
        return


# end of file
