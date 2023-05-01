# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .Fragment import Fragment


# the directory structure of the build
class Layout(Fragment):
    """
    The generator of the makefile with the directory structure of the build
    """

    # configurable state
    makefile = merlin.properties.path()
    makefile.default = "layout"
    makefile.doc = "the generated makefile"

    # interface
    def generate(self, stage, **kwds):
        """
        Generate my makefile
        """
        # build the makefile path
        makefile = stage / "merlin" / self.makefile
        # an identifying comment
        marker = "the directory layout"
        # chain up
        yield from super().generate(makefile=makefile, marker=marker, **kwds)

    # implementation details
    def _generate(self, layout, **kwds):
        """
        Build my contents
        """
        # chain up
        yield from super()._generate(**kwds)
        # make the assignments
        yield from self._assignments(layout=layout)
        # build the rules
        yield from self._rules(layout=layout)
        # all done
        return

    def _assignments(self, layout):
        """
        Record the layout
        """
        # get my renderer
        renderer = self.renderer
        # record the directory layout of the {/workspace}
        # get the node
        ws = self.pyre_fileserver["/workspace"]
        # sign on
        yield ""
        yield renderer.commentLine("workspace layout")
        # save the value
        yield from renderer.set(name="ws", value=f"{ws.uri}")
        # get the stage
        stage = self.pyre_fileserver["/stage"]
        # make a mark
        yield renderer.commentLine("the staging directory")
        # save the value
        yield from renderer.set(name="stage", value=f"{stage.uri}")
        # make a mark
        yield renderer.commentLine("the cloned sources")
        # save the value
        yield from renderer.set(name="src", value=f"$(stage)/src")
        # form the path to the build directory
        build = stage.uri / "build"
        # make a mark
        yield renderer.commentLine("the build directory")
        # save the value
        yield from renderer.set(name="build", value=f"$(stage)/build")
        # make some room
        yield ""

        # specify the directory layout of the {/prefix}
        yield renderer.commentLine("prefix layout")
        # get the root of the prefix tree
        prefix = self.pyre_fileserver["/prefix"]
        yield from renderer.set(name="prefix", value=f"{prefix.uri}")
        # go through my layout
        for trait in layout.pyre_configurables():
            # the trait name specifies the mount point in the virtual filesystem
            name = trait.name
            # and its value is the path under {/prefix} in the physical filesystem
            relpath, _ = layout.pyre_getTrait(alias=name)
            # generate the assignment
            yield from renderer.set(name=f"prefix.{name}", value=f"$(prefix)/{relpath}")

        # all done
        return

    def _rules(self, layout):
        """
        Build rules that generate the {/prefix} directory structure
        """
        # get my renderer
        renderer = self.renderer

        # the directory with the cloned sources
        yield ""
        yield renderer.commentLine(f"make /stage/src")
        # the dependency line
        yield f"$(src):"
        # log
        yield f"\t@$(call log.action,mkdir,/stage/src)"
        # the rule
        yield f"\t@$(mkdirp) $@"

        # the directory with the build artifacts
        yield ""
        yield renderer.commentLine(f"make /stage/build")
        # the dependency line
        yield f"$(build):"
        # log
        yield f"\t@$(call log.action,mkdir,/stage/build)"
        # the rule
        yield f"\t@$(mkdirp) $@"

        # build the canonical location for the prefix
        prefix = merlin.primitives.path("/prefix")
        # its entire configurable state is supposed to be subdirectories of {/prefix}, so
        # go through it
        for trait in layout.pyre_configurables():
            # the trait name specifies the mount point in the virtual filesystem
            name = trait.name
            # and its value is the path under {/prefix} in the physical filesystem
            path, _ = layout.pyre_getTrait(alias=name)
            # build the physical path using the variable from the layout
            dir = f"$(prefix.{name})"
            # and project it to its logical location to make a tag
            tag = prefix / path
            # sign on
            yield ""
            yield renderer.commentLine(f"make {tag}")
            # the dependency line
            yield f"{dir}:"
            # log
            yield f"\t@$(call log.action,mkdir,{tag})"
            # the rule
            yield f"\t@$(mkdirp) $@"

        # all done
        return


# end of file
