# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the environment variables
import os


# maps of color names to the ANSI control sequences that render them; the sequences are produced
# by {pyre::chroma}, exposed to python as {pyre.libpyre.chroma}
class ANSI:
    """
    Mappings from color names to ANSI control sequences, backed by the {chroma} color bindings
    """

    # interface
    @classmethod
    def compatible(cls):
        """
        Attempt to assess whether the current terminal is ANSI compatible
        """
        # read the {TERM} environment variable, assuming a dumb terminal when it is unset
        term = os.environ.get("TERM", "dumb").lower()
        # the terminal is compatible when its type is one we recognize
        return term in cls._compatible

    @classmethod
    def null(cls, name):
        """
        The null colorspace, where every color maps to an empty string
        """
        # nothing is ever colored here
        return ""

    @classmethod
    def ansi(cls, name):
        """
        Return the control sequence for the 16-color terminal-palette {name}
        """
        # reach the color bindings
        chroma = cls._chroma()
        # without them there is no color
        if chroma is None:
            return ""
        # {normal} restores the terminal defaults
        if name == "normal":
            return chroma.ansi.reset()
        # look up the terminal-palette code and brightness for this name
        code = cls._codes.get(name)
        # an unknown name produces no color
        if code is None:
            return ""
        # render the code through chroma
        return chroma.ansi.csi3(code[0], code[1])

    @classmethod
    def gray(cls, name):
        """
        Return the control sequence for the named gray {name}
        """
        # the grays are ordinary named colors
        return cls._named(name)

    @classmethod
    def x11(cls, name):
        """
        Return the control sequence for the X11 color {name}
        """
        # the X11 colors live in chroma's palette
        return cls._named(name)

    @classmethod
    def misc(cls, name):
        """
        Return the control sequence for pyre's custom color {name}
        """
        # pyre's colors also live in chroma's palette
        return cls._named(name)

    # implementation details
    @classmethod
    def _named(cls, name):
        """
        Render a named color as a 24-bit escape via {chroma}; {normal} means reset
        """
        # reach the color bindings
        chroma = cls._chroma()
        # without them there is no color
        if chroma is None:
            return ""
        # {normal} restores the terminal defaults rather than naming a color
        if name == "normal":
            return chroma.ansi.reset()
        # look the name up in chroma's palette
        color = chroma.rgb.palette.find(name)
        # an unknown name produces no color
        if color is None:
            return ""
        # a known name renders as a 24-bit truecolor escape
        return chroma.ansi.rgb(color)

    @classmethod
    def _chroma(cls):
        """
        Access the {chroma} color bindings, or {None} when they are unavailable (e.g. bootstrap)
        """
        # the framework carries the bindings
        import pyre

        # they live on {libpyre}, which is absent when the extension was not built
        return None if pyre.libpyre is None else pyre.libpyre.chroma

    # the 16-color names mapped to their terminal-palette codes and bright flags
    _codes = {
        # regular colors
        "black": (30, False),
        "red": (31, False),
        "green": (32, False),
        "brown": (33, False),
        "blue": (34, False),
        "purple": (35, False),
        "cyan": (36, False),
        "light-gray": (37, False),
        # bright colors
        "dark-gray": (30, True),
        "light-red": (31, True),
        "light-green": (32, True),
        "yellow": (33, True),
        "light-blue": (34, True),
        "light-purple": (35, True),
        "light-cyan": (36, True),
        "white": (37, True),
    }

    # the set of terminal types that understand ANSI control sequences
    _compatible = {
        "ansi",
        "vt102",
        "vt220",
        "vt320",
        "vt420",
        "xterm",
        "xterm-color",
        "xterm-16color",
        "xterm-256color",
    }


# end of file
