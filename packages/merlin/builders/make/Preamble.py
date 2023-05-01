# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .Fragment import Fragment


# the preamble with the makefile boilerplate
class Preamble(Fragment):
    """
    The generator of the makefile with the boilerplate support
    """

    # configurable state
    makefile = merlin.properties.path()
    makefile.default = "preamble"
    makefile.doc = "the generated makefile"

    # interface
    def generate(self, stage, **kwds):
        """
        Generate my makefile
        """
        # build the makefile path
        makefile = stage / "merlin" / self.makefile
        # and a comment
        marker = f"boilerplate"
        # chain up
        yield from super().generate(makefile=makefile, marker=marker, **kwds)

    # implementation details
    def _generate(self, target="projects", **kwds):
        """
        Build my contents
        """
        # chain up
        yield from super()._generate(**kwds)
        # makefile prep
        yield from self._prep(target=target)
        # basic tokens to eliminate ambiguities and errors
        yield from self._tokens()
        # setup color support
        yield from self._color()
        # screen logs
        yield from self._screen()
        # commonly used tools
        yield from self._tools()
        # all done
        return

    def _prep(self, target):
        """
        Miscellaneous makefile prep
        """
        # get my renderer
        renderer = self.renderer
        # sign on
        yield ""
        yield renderer.commentLine("prep")
        # the default target
        yield from renderer.set(name=".DEFAULT_GOAL", value=target)

    def _tokens(self):
        """
        Simple variables that eliminate ambiguities and errors
        """
        # get my renderer
        renderer = self.renderer
        # sign on
        yield ""
        yield renderer.commentLine("tokens")
        # simple tokens
        yield from renderer.set(name="empty")
        yield from renderer.set(name="comma", value=",")
        yield from renderer.set(name="space", value="$(empty) $(empty)")

        # characters that don't render easily and make the makefile less readable
        yield from renderer.set(name="esc", value='"\x1b"')

        # all done
        return

    def _color(self):
        """
        Set up support for colorized output
        """
        # get my renderer
        renderer = self.renderer
        # sign on
        yield ""
        yield renderer.commentLine("color support")

        # sniff the terminal type
        yield renderer.commentLine("initialize the TERM environment variable")
        yield from renderer.setu(name="TERM", value="dumb")

        # build a conditional assignment block so we can turn color off on terminals that
        # don't understand ANSI control sequences
        yield from renderer.ifeq(
            op1=renderer.value(var="TERM"),
            op2=renderer.builtin(
                func="findstring",
                args=[renderer.value(var="TERM"), self._ansiTerminals],
            ),
            onTrue=self._ansiCSI(),
            onFalse=self._dumbCSI(),
        )

        # render the color database
        # basic colors
        yield ""
        yield renderer.commentLine("basic colors")
        yield from renderer.set(
            name="palette.normal", value=renderer.call(func="csi3", args=["0"])
        )
        yield from renderer.set(
            name="palette.black", value=renderer.call(func="csi3", args=["0;30"])
        )
        yield from renderer.set(
            name="palette.red", value=renderer.call(func="csi3", args=["0;31"])
        )
        yield from renderer.set(
            name="palette.green", value=renderer.call(func="csi3", args=["0;32"])
        )
        yield from renderer.set(
            name="palette.brown", value=renderer.call(func="csi3", args=["0;33"])
        )
        yield from renderer.set(
            name="palette.blue", value=renderer.call(func="csi3", args=["0;34"])
        )
        yield from renderer.set(
            name="palette.purple", value=renderer.call(func="csi3", args=["0;35"])
        )
        yield from renderer.set(
            name="palette.cyan", value=renderer.call(func="csi3", args=["0;36"])
        )
        yield from renderer.set(
            name="palette.light-gray", value=renderer.call(func="csi3", args=["0;37"])
        )

        # bright colors
        yield ""
        yield renderer.commentLine("bright colors")
        yield from renderer.set(
            name="palette.dark-gray", value=renderer.call(func="csi3", args=["1;30"])
        )
        yield from renderer.set(
            name="palette.light-red", value=renderer.call(func="csi3", args=["1;31"])
        )
        yield from renderer.set(
            name="palette.light-green", value=renderer.call(func="csi3", args=["1;32"])
        )
        yield from renderer.set(
            name="palette.yellow", value=renderer.call(func="csi3", args=["1;33"])
        )
        yield from renderer.set(
            name="palette.light-blue", value=renderer.call(func="csi3", args=["1;34"])
        )
        yield from renderer.set(
            name="palette.light-purple", value=renderer.call(func="csi3", args=["1;35"])
        )
        yield from renderer.set(
            name="palette.light-cyan", value=renderer.call(func="csi3", args=["1;36"])
        )
        yield from renderer.set(
            name="palette.white", value=renderer.call(func="csi3", args=["1;37"])
        )

        # pretty colors
        yield ""
        yield renderer.commentLine("pretty colors")
        yield from renderer.set(
            name="palette.amber",
            value=renderer.call(func="csi24", args=["38", "255", "191", "0"]),
        )
        yield from renderer.set(
            name="palette.lavender",
            value=renderer.call(func="csi24", args=["38", "192", "176", "224"]),
        )
        yield from renderer.set(
            name="palette.sage",
            value=renderer.call(func="csi24", args=["38", "176", "208", "176"]),
        )
        yield from renderer.set(
            name="palette.steel-blue",
            value=renderer.call(func="csi24", args=["38", "70", "130", "180"]),
        )

        # diagnostics
        yield ""
        yield renderer.commentLine("diagnostics")
        yield from renderer.set(
            name="palette.info", value=renderer.call(func="csi8", args=["38", "28"])
        )
        yield from renderer.set(
            name="palette.warning", value=renderer.call(func="csi8", args=["38", "214"])
        )
        yield from renderer.set(
            name="palette.error", value=renderer.call(func="csi8", args=["38", "196"])
        )
        yield from renderer.set(
            name="palette.debug", value=renderer.call(func="csi8", args=["38", "75"])
        )
        yield from renderer.set(
            name="palette.firewall", value=renderer.value(var="palette.light-red")
        )

        # the default theme
        yield ""
        yield renderer.commentLine("the default theme")
        yield from renderer.set(
            name="palette.asset", value=renderer.value(var="palette.steel-blue")
        )
        yield from renderer.set(
            name="palette.action", value=renderer.value(var="palette.lavender")
        )
        yield from renderer.set(
            name="palette.attention", value=renderer.value(var="palette.purple")
        )

        # all done
        return

    def _screen(self):
        """
        Support for colorized screen output
        """
        yield ""
        yield "# screen functions"
        yield "log ?= echo"
        yield "# indentation"
        yield 'log.halfdent := "  "'
        yield 'log.indent := "    "'
        yield ""
        yield "log.info = \\"
        yield "    $(log) \\"
        yield '    $(palette.info)"  [info]"$(palette.normal) \\'
        yield "    $(palette.info)$(1)$(palette.normal)"
        yield ""
        yield "log.warning = \\"
        yield "    $(log) \\"
        yield '    $(palette.warning)"  [warning]"$(palette.normal) \\'
        yield "    $(palette.warning)$(1)$(palette.normal)"
        yield ""
        yield "log.error = \\"
        yield "    $(log) \\"
        yield '    $(palette.error)"  [error]"$(palette.normal) \\'
        yield "    $(palette.error)$(1)$(palette.normal)"
        yield ""
        yield "log.debug = \\"
        yield "    $(log) \\"
        yield '    $(palette.debug)"  [debug]"$(palette.normal) \\'
        yield "    $(palette.debug)$(1)$(palette.normal)"
        yield ""
        yield "log.firewall = \\"
        yield "    $(log) \\"
        yield '    $(palette.firewall)"  [firewall]"$(palette.normal) \\'
        yield "    $(palette.firewall)$(1)$(palette.normal)"
        yield ""
        yield "# render a build action"
        yield "log.asset = \\"
        yield "    $(log) \\"
        yield '    $(palette.asset)"  [$(1)]"$(palette.normal) \\'
        yield "    $(2)"
        yield ""
        yield "log.action = \\"
        yield "    $(log) \\"
        yield '    $(palette.action)"  [$(1)]"$(palette.normal) \\'
        yield "    $(2)"
        yield ""
        yield "log.attention = \\"
        yield "    $(log) \\"
        yield '    $(palette.attention)"  [$(1)]"$(palette.normal) \\'
        yield "    $(2)"
        yield ""
        # all done
        return

    def _tools(self):
        """
        Set up macros for accessing the toolchain
        """
        # sign on
        yield ""
        yield "# tools"
        yield "# librarian"
        yield "ar := ar"
        yield "ar.flags.create := rc"
        yield "ar.flags.extract := x"
        yield "ar.flags.remove := d"
        yield "ar.flags.update := ru"
        yield "ar.create := $(ar) $(ar.flags.create)"
        yield "ar.extract := $(ar) $(ar.flags.extract)"
        yield "ar.remove := $(ar) $(ar.flags.remove)"
        yield "ar.update := $(ar) $(ar.flags.update)"
        yield ""
        yield "# cwd"
        yield "cd := cd"
        yield ""
        yield "# file attributes"
        yield "chgrp := chgrp"
        yield "chgrp.flags.recurse := -R"
        yield "chgrp.recurse := $(chgrp) $(chgrp.flags.recurse)"
        yield ""
        yield "chmod := chmod"
        yield "chmod.flags.recurse := -R"
        yield "chmod.flags.write := +w"
        yield "chmod.recurse := $(chmod) $(chmod.flags.recurse)"
        yield "chmod.write := $(chmod) $(chmod.flags.write)"
        yield "chmod.write-recurse := $(chmod.recurse) $(chmod.flags.write)"
        yield ""
        yield "chown := chown"
        yield "chown.flags.recurse := -R"
        yield "chown.recurse := $(chown) $(chown.flags.recurse)"
        yield ""
        yield "# copy"
        yield "cp := cp"
        yield "cp.flags.force := -f"
        yield "cp.flags.recurse := -r"
        yield "cp.flags.force-recurse := -fr"
        yield "cp.force := $(cp) $(cp.flags.force)"
        yield "cp.recurse := $(cp) $(cp.flags.recurse)"
        yield "cp.force-recurse := $(cp) $(cp.flags.force-recurse)"
        yield ""
        yield "# date"
        yield "date := date"
        yield "date.date := $(date) '+%Y-%m-%d'"
        yield "date.stamp := $(date) -u"
        yield "date.year := $(date) '+%Y'"
        yield ""
        yield "# diff"
        yield "diff := diff"
        yield ""
        yield "# echo"
        yield "echo := echo"
        yield ""
        yield "# git"
        yield "git := git"
        yield 'git.hash := $(git) log --format=format:"%h" -n 1'
        yield "git.tag := $(git) describe --tags --long --always"
        yield ""
        yield "# loader"
        yield "ld := ld"
        yield "ld.flags.out :=  -o"
        yield "ld.flags.shared :=  -shared"
        yield "ld.out := $(ld) $(ld.flags.out)"
        yield "ld.shared := $(ld) $(ld.flags.shared)"
        yield ""
        yield "# links"
        yield "ln := ln"
        yield "ln.flags.soft := -s"
        yield "ln.soft := $(ln) $(ln.flags.soft)"
        yield ""
        yield "# directories"
        yield "mkdir := mkdir"
        yield "mkdir.flags.make-parents := -p"
        yield "mkdirp := $(mkdir) $(mkdir.flags.make-parents)"
        yield ""
        yield "# move"
        yield "mv := mv"
        yield "mv.flags.force := -f"
        yield "mv.force := $(mv) $(mv.flags.force)"
        yield ""
        yield "# ranlib"
        yield "ranlib := ranlib"
        yield "ranlib.flags :="
        yield ""
        yield "# remove"
        yield "rm := rm"
        yield "rm.flags.force := -f"
        yield "rm.flags.recurse := -r"
        yield "rm.flags.force-recurse := -rf"
        yield "rm.force := $(rm) $(rm.flags.force)"
        yield "rm.recurse := $(rm) $(rm.flags.recurse)"
        yield "rm.force-recurse := $(rm) $(rm.flags.force-recurse)"
        yield ""
        yield "rmdir := rmdir"
        yield ""
        yield "# rsync"
        yield "rsync := rsync"
        yield "rsync.flags.recurse := -ruavz --progress --stats"
        yield "rsync.recurse := $(rsync) $(rsync.flags.recurse)"
        yield ""
        yield "# sed"
        yield "sed := sed"
        yield ""
        yield "# ssh"
        yield "ssh := ssh"
        yield "scp := scp"
        yield "scp.flags.recurse := -r"
        yield "scp.recurse := $(scp) $(scp.flags.recurse)"
        yield ""
        yield "# tags"
        yield "tags := true"
        yield "tags.flags :="
        yield "tags.home :="
        yield "tags.file := $(tags.home)/TAGS"
        yield ""
        yield "# tar"
        yield "tar := tar"
        yield "tar.flags.create := -cvj -f"
        yield "tar.create := $(tar) $(tar.flags.create)"
        yield ""
        yield "# TeX and associated tools"
        yield "tex.tex := tex"
        yield "tex.latex := latex"
        yield "tex.pdflatex := pdflatex"
        yield "tex.bibtex := bibtex"
        yield "tex.dvips := dvips"
        yield "tex.dvipdf := dvipdf"
        yield ""
        yield "# empty file creation and modification time updates"
        yield "touch := touch"
        yield ""
        yield "# yacc"
        yield "yacc := yacc"
        yield "yacc.c := y.tab.c"
        yield "yacc.h := y.tab.h"

        # all done
        return

    # helpers
    def _ansiCSI(self):
        """
        Build function that construct the ANSI control sequences
        """
        # get my renderer
        renderer = self.renderer
        # build the 3 bit color generator
        yield from renderer.setq(name="csi3", value=f'"$(esc)[$(1)m"')
        yield from renderer.setq(name="csi8", value=f'"$(esc)[$(1);5;$(2)m"')
        yield from renderer.setq(name="csi24", value=f'"$(esc)[$(1);2;$(2);$(3);$(4)m"')

        # all done
        return

    def _dumbCSI(self):
        """
        Build function that construct stubs for the ANSI control sequences
        """
        # get my renderer
        renderer = self.renderer
        # build the 3 bit color generator
        yield from renderer.set(name="csi3", value="")
        yield from renderer.set(name="csi8", value="")
        yield from renderer.set(name="csi24", value="")

        # all done
        return

    def _makeColor(self, renderer, name, space, color):
        """
        Build the expression that creates a color
        """
        # assemble the arguments
        args = (renderer.literal(value) for value in color)
        # build and return the expression
        return renderer.set(name=name, value=renderer.call(func=space, args=args))

    # constants
    _ansiTerminals = "ansi vt100 vt102 xterm xterm-color xterm-256color"


# end of file
