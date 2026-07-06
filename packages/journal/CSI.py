# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, for the {chroma} color bindings
import pyre


# reach the {chroma} color bindings, or {None} when they are unavailable (e.g. during bootstrap)
def _chroma():
    # the bindings live on {libpyre}, which is absent when the extension was not built
    return None if pyre.libpyre is None else pyre.libpyre.chroma


# a generator of ANSI control strings; all color sequences are delegated to {pyre::chroma}
class CSI:
    """
    A generator of ANSI control strings, backed by the {chroma} color bindings
    """

    # reset
    @staticmethod
    def reset():
        """
        Reset all output attributes
        """
        # reach the bindings
        chroma = _chroma()
        # delegate, or produce nothing when they are unavailable
        return chroma.ansi.reset() if chroma is not None else ""

    # the color commands
    @staticmethod
    def csi3(code=None, bright=False):
        """
        Build a 16-color ANSI control sequence
        """
        # reach the bindings
        chroma = _chroma()
        # delegate the terminal-palette code
        return chroma.ansi.csi3(code, bright) if chroma is not None else ""

    @staticmethod
    def csi8(red=0, green=0, blue=0, foreground=True):
        """
        Build a 256-color-cube control sequence from channels in [0, 5]
        """
        # reach the bindings
        chroma = _chroma()
        # without them there is no color
        if chroma is None:
            return ""
        # normalize the cube coordinates and let chroma quantize them back
        return chroma.ansi.rgb256(
            chroma.Color(red / 5, green / 5, blue / 5), foreground
        )

    @staticmethod
    def csi8_gray(gray=0, foreground=True):
        """
        Build a grayscale-ramp control sequence from a step in [0, 23]
        """
        # reach the bindings
        chroma = _chroma()
        # without them there is no color
        if chroma is None:
            return ""
        # normalize the ramp step and let chroma quantize it back
        return chroma.ansi.gray(gray / 23, foreground)

    @staticmethod
    def csi24(red=0, green=0, blue=0, foreground=True):
        """
        Build a 24-bit truecolor control sequence from channels in [0, 255]
        """
        # reach the bindings
        chroma = _chroma()
        # without them there is no color
        if chroma is None:
            return ""
        # normalize the channels and hand them to chroma as a color
        return chroma.ansi.rgb(
            chroma.Color(red / 255, green / 255, blue / 255), foreground
        )

    # graphics rendition commands
    @staticmethod
    def blink(state=True):
        """
        Turn blink on or off
        """
        # blink is a text style, not a color, so chroma does not cover it; build it locally
        return f"\x1b[{'5' if state else '25'}m"


# end of file
