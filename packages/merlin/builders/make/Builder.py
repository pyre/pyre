# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import datetime
# support
import merlin

# my superclass
from ..Builder import Builder as BaseBuilder


# the manager of intermediate and final build products
class Builder(BaseBuilder, family="merlin.builders.make"):
    """
    The manager of the all build products, both final and intermediate disposables
    """


    # configurable state
    renderer = merlin.weaver.language()
    renderer.default = "make"
    renderer.doc = "the makefile mill"


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
        # and the root of the virtual filesystem
        vfs = plexus.vfs

        # prep the stage area
        self.setupStage(vfs=vfs, abi=abi)
        # and the prefix
        self.setupPrefix(vfs=vfs, abi=abi)

        # all done
        return


    # implementation details
    def setupStage(self, vfs, abi):
        """
        Set up the staging area for build temporaries
        """
        # get the user's home directory
        home = self.pyre_user.home
        # and the workspace path
        ws = vfs["/workspace"].uri
        # attempt to
        try:
            # project the workspace onto the user's home
            rel = ws.relativeTo(home)
        # if this fails
        except ValueError:
            # just use the trailing part of the workspace
            rel = [ws.name]

        # we will hash the workspace
        wshash = "~".join(rel)

        # build the stage path
        stage = self.stage / wshash / abi / self.tag
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


    def setupPrefix(self, vfs, abi):
        """
        Set up the installation area
        """
        # check whether the users wants the ABI folded into the prefix
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
        yield ""

        # all done
        return


    def rules(self, renderer, assets, **kwds):
        """
        Generate the makefile preamble with all the boilerplate code
        """
        # sign on
        yield ""
        yield renderer.commentLine("rules")

        # collect the names of the assets
        names = ' '.join(asset.pyre_name for asset in assets)
        # make a rule that builds them all
        yield f"all: {names}"
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


    # asset visitors
    def library(self, library):
        """
        Build a {library}
        """
        # do nothing, for now
        return


    # constants
    ansiTerminals = " ".join([ "ansi", "vt100", "vt102", "xterm", "xterm-color", "xterm-256color" ])


# end of file
