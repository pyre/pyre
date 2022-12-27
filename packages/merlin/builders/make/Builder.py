# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import datetime
# support
import merlin

# my superclass
from ..Builder import Builder as BaseBuilder
# my parts
from .LibFlow import LibFlow


# the manager of intermediate and final build products
class Builder(BaseBuilder, family="merlin.builders.make"):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # configurable state
    renderer = merlin.weaver.language()
    renderer.default = "make"
    renderer.doc = "the makefile mill"

    libflow = merlin.protocols.libflow()
    libflow.default = LibFlow
    libflow.doc = "the library workflow generator"


    # interface
    def add(self, plexus, **kwds):
        """
        Add the given assets to the build pile
        """
        # grab the stage uri
        stage = plexus.vfs["/stage"].uri
        # form the path to the makefile
        makefile = stage / "Makefile"

        # open the stream
        with open(makefile, mode="w") as stream:
            # grab my renderer
            renderer = self.renderer
            # prime the makefile content
            document = self.generate(plexus=plexus, renderer=renderer, **kwds)
            # ask the renderer to do its thing
            content = renderer.render(document=document)
            # and write
            print('\n'.join(content), file=stream)

        # all done
        return


    # framework hooks
    def merlin_initialized(self, plexus, **kwds):
        """
        Hook invoked after the {plexus} is fully initialized
        """
        # chain up
        super().merlin_initialized(plexus=plexus, **kwds)

        # grab my abi
        abi = self.abi(plexus=plexus)

        # prep the stage area
        self.setupStage(plexus=plexus, abi=abi, **kwds)
        # and the prefix
        self.setupPrefix(plexus=plexus, abi=abi, **kwds)

        # all done
        return


    # asset visitors
    def library(self, **kwds):
        """
        Build a {library}
        """
        # delegate to the {libflow} generator
        return self.libflow.library(builder=self, **kwds)


    # implementation details
    def setupStage(self, plexus, abi, **kwds):
        """
        Set up the staging area for build temporaries
        """
        # get the root of the virtual filesystem
        vfs = plexus.vfs
        # hash the workspace into a build tag
        wstag = self.workspaceHash(plexus=plexus)
        # build the stage path
        stage = self.stage / wstag / abi / self.tag
        # force the creation of the directory
        stage.mkdir(parents=True, exist_ok=True)
        # use it to anchor a local filesystem
        stageFS = vfs.retrieveFilesystem(root=stage)
        # build the canonical location for the stage in the virtual filesystem
        stagePath = merlin.primitives.path("/stage")
        # and mount it at its canonical location
        vfs[stagePath] = stageFS

        # all done
        return


    def setupPrefix(self, plexus, abi, **kwds):
        """
        Set up the installation area
        """
        # get the root of the virtual filesystem
        vfs = plexus.vfs
        # check whether the user wants the ABI folded into the prefix
        prefix = self.prefix / abi / self.tag if self.tagged else self.prefix
        # force the creation of the actual directory
        prefix.mkdir(parents=True, exist_ok=True)
        # use it as an anchor for a local filesystem
        prefixFS = vfs.retrieveFilesystem(root=prefix)
        # build the canonical location for the prefix
        prefixPath = merlin.primitives.path("/prefix")
        # and mount the filesystem there
        vfs[prefixPath] = prefixFS
        # all done
        return


    # makefile generation
    def generate(self, **kwds):
        """
        Generate the makefile
        """
        # preamble
        yield from self.preamble(**kwds)
        # build rules
        yield from self.rules(**kwds)
        # boiler plate support
        yield from self.boilerplate(**kwds)
        # postamble
        yield from self.postamble(**kwds)
        # all done
        return


    def preamble(self, renderer, **kwds):
        """
        Generate the makefile preamble with all the boilerplate code
        """
        # make a time stamp
        stamp = f"generated on {datetime.datetime.now().isoformat()}"
        # mark
        yield renderer.commentLine(stamp)

        # record the directory layout of the {/workspace}
        # get the node
        ws = self.pyre_fileserver["/workspace"]
        # sign on
        yield ""
        yield renderer.commentLine("workspace layout")
        # save the value
        yield from renderer.set(name="ws", value=f"{ws.uri}")

        # record the location of the {/stage}
        # get the node
        stage = self.pyre_fileserver["/stage"]
        yield ""
        yield renderer.commentLine("stage layout")
        # save the value
        yield from renderer.set(name="stage", value=f"{stage.uri}")

        # specify the directory layout of the {/prefix}
        yield ""
        yield renderer.commentLine("prefix layout")
        # get my layout
        layout = self.layout
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
            yield from renderer.set(name=f"prefix.{name}", value=f"${{prefix}}/{relpath}")

        # all done
        return


    def rules(self, renderer, assets, **kwds):
        """
        Generate the makefile preamble with all the boilerplate code
        """
        # sign on
        yield ""
        yield renderer.commentLine("rules")

        # concretize the asset sequence because we traverse it multiple times
        assets = tuple(assets)

        # collect the names of the assets
        names = ' '.join(asset.pyre_name for asset in assets)
        # make a rule that builds them all
        yield f"all: {names}"

        # now go through them
        for asset in assets:
            # and process each one
            yield from asset.identify(visitor=self, renderer=renderer, **kwds)

        # set up the {/prefix} directory layout
        yield from self.prefixRules(renderer=renderer, assets=assets, **kwds)

        # all done
        return


    def prefixRules(self, renderer, **kwds):
        """
        Build rules that generate the {/prefix} directory structure
        """
        # build the canonical location for the prefix
        prefixPath = merlin.primitives.path("/prefix")
        # and get the actual node
        prefix = self.pyre_fileserver[prefixPath]

        # sign on
        yield ""
        yield renderer.commentLine(f"/prefix directory layout")

        # grab my layout
        layout = self.layout
        # its entire configurable state is supposed to be subdirectories of {/prefix}, so
        # go through it
        for trait in layout.pyre_configurables():
            # the trait name specifies the mount point in the virtual filesystem
            name = trait.name
            # and its value is the path under {/prefix} in the physical filesystem
            relpath, _ = layout.pyre_getTrait(alias=name)
            # build its physical path
            path = prefix.uri / relpath
            # and project it to its canonical location to make a tag
            tag = prefixPath / relpath
            # sign on
            yield ""
            yield renderer.commentLine(f"make {tag}")
            # the dependency line
            yield f"{path}:"
            # log
            yield f"\t@echo [mkdir] {tag}"
            # the rule
            yield f"\t@mkdir -p $@"

        # all done
        return


    def boilerplate(self, renderer, **kwds):
        """
        Generate the makefile preamble with all the boilerplate code
        """
        # sign on
        yield ""
        # basic tokens to eliminate ambiguities and errors
        yield from self.tokens(renderer, **kwds)
        # setup color support
        yield from self.color(renderer, **kwds)
        # all done
        return


    def postamble(self, renderer, **kwds):
        """
        Generate the makefile preamble with all the boilerplate code
        """
        # sign on
        yield ""
        # all done
        return


    def color(self, renderer, **kwds):
        """
        Set up support for colorized output
        """
        # sign on
        yield ""
        yield renderer.commentLine("color support")

        # sniff the terminal type
        yield renderer.commentLine("initialize the TERM environment variable")
        yield from renderer.setu(name="TERM", value="dumb")

        # build a conditional assignment block so we can turn color off on terminals that
        # don't understand ANSI control sequences
        yield from renderer.ifeq(
            op1 = renderer.value(var="TERM"),
            op2 = renderer.builtin(func="findstring",
                                   args=[renderer.value(var="TERM"), self.ansiTerminals]),
            onTrue = self.ansiCSI(renderer, **kwds),
            onFalse = self.dumbCSI(renderer, **kwds),
        )

        # render the color database
        # basic colors
        yield ""
        yield renderer.commentLine("basic colors")
        yield from renderer.set(name="palette.normal",
                                value=renderer.call(func="csi3", args=["0"]))
        yield from renderer.set(name="palette.black",
                                value=renderer.call(func="csi3", args=["0;30"]))
        yield from renderer.set(name="palette.red",
                                value=renderer.call(func="csi3", args=["0;31"]))
        yield from renderer.set(name="palette.green",
                                value=renderer.call(func="csi3", args=["0;32"]))
        yield from renderer.set(name="palette.brown",
                                value=renderer.call(func="csi3", args=["0;33"]))
        yield from renderer.set(name="palette.blue",
                                value=renderer.call(func="csi3", args=["0;34"]))
        yield from renderer.set(name="palette.purple",
                                value=renderer.call(func="csi3", args=["0;35"]))
        yield from renderer.set(name="palette.cyan",
                                value=renderer.call(func="csi3", args=["0;36"]))
        yield from renderer.set(name="palette.light-gray",
                                value=renderer.call(func="csi3", args=["0;37"]))

        # bright colors
        yield ""
        yield renderer.commentLine("bright colors")
        yield from renderer.set(name="palette.dark-gray",
                                value=renderer.call(func="csi3", args=["1;30"]))
        yield from renderer.set(name="palette.light-red",
                                value=renderer.call(func="csi3", args=["1;31"]))
        yield from renderer.set(name="palette.light-green",
                                value=renderer.call(func="csi3", args=["1;32"]))
        yield from renderer.set(name="palette.yellow",
                                value=renderer.call(func="csi3", args=["1;33"]))
        yield from renderer.set(name="palette.light-blue",
                                value=renderer.call(func="csi3", args=["1;34"]))
        yield from renderer.set(name="palette.light-purple",
                                value=renderer.call(func="csi3", args=["1;35"]))
        yield from renderer.set(name="palette.light-cyan",
                                value=renderer.call(func="csi3", args=["1;36"]))
        yield from renderer.set(name="palette.white",
                                value=renderer.call(func="csi3", args=["1;37"]))

        # pretty colors
        yield ""
        yield renderer.commentLine("pretty colors")
        yield from renderer.set(name="palette.amber",
                                value=renderer.call(func="csi24", args=["38", "255", "191", "0"]))
        yield from renderer.set(name="palette.lavender",
                                value=renderer.call(func="csi24", args=["38", "192", "176", "224"]))
        yield from renderer.set(name="palette.sage",
                                value=renderer.call(func="csi24", args=["38", "176", "208", "176"]))
        yield from renderer.set(name="palette.steel-blue",
                                value=renderer.call(func="csi24", args=["38", "70", "130", "180"]))

        # diagnostics
        yield ""
        yield renderer.commentLine("diagnostics")
        yield from renderer.set(name="palette.info",
                                value=renderer.call(func="csi8", args=["38", "28"]))
        yield from renderer.set(name="palette.warning",
                                value=renderer.call(func="csi8", args=["38", "214"]))
        yield from renderer.set(name="palette.error",
                                value=renderer.call(func="csi8", args=["38", "196"]))
        yield from renderer.set(name="palette.debug",
                                value=renderer.call(func="csi8", args=["38", "75"]))
        yield from renderer.set(name="palette.firewall",
                                value=renderer.value(var="palette.light-red"))

        # the default theme
        yield ""
        yield renderer.commentLine("the default theme")
        yield from renderer.set(name="palette.asset",
                                value=renderer.value(var="palette.steel-blue"))
        yield from renderer.set(name="palette.action",
                                value=renderer.value(var="palette.lavender"))
        yield from renderer.set(name="palette.attention",
                                value=renderer.value(var="palette.purple"))

        # all done
        return


    def tokens(self, renderer, **kwds):
        """
        Simple variables that eliminate ambiguities and errors
        """
        # sign on
        yield ""
        yield renderer.commentLine("tokens")
        # simple tokens
        yield from renderer.set(name="empty")
        yield from renderer.set(name="comma", value=",")
        yield from renderer.set(name="space", value="$(empty) $(empty)")

        # characters that don't render easily and make the makefile less readable
        yield from renderer.set(name="esc", value="\"\x1b\"")

        # all done
        return


    # helpers
    def ansiCSI(self, renderer, **kwds):
        """
        Build function that construct the ANSI control sequences
        """
        # build the 3 bit color generator
        yield from renderer.setq(name="csi3", value=f"\"$(esc)[$(1)m\"")
        yield from renderer.setq(name="csi8", value=f"\"$(esc)[$(1);5;$(2)m\"")
        yield from renderer.setq(name="csi24", value=f"\"$(esc)[$(1);2;$(2);$(3);$(4)m\"")

        # all done
        return


    def dumbCSI(self, renderer, **kwds):
        """
        Build function that construct stubs for the ANSI control sequences
        """
        # build the 3 bit color generator
        yield from renderer.set(name="csi3", value="")
        yield from renderer.set(name="csi8", value="")
        yield from renderer.set(name="csi24", value="")

        # all done
        return


    def makeColor(self, renderer, name, space, color):
        """
        Build the expression that creates a color
        """
        # assemble the arguments
        args = (renderer.literal(value) for value in color)
        # build and return the expression
        return renderer.set(name=name, value=renderer.call(func=space, args=args))


    # constants
    ansiTerminals = "ansi vt100 vt102 xterm xterm-color xterm-256color"


# end of file
