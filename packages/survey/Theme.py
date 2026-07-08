# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import math

# the framework, for the color bindings
import pyre


class Theme:
    """
    The palette a prompt paints with: the message, the pointer, the current choice, the hint;
    each entry is a {chroma} color, or {None} for no color
    """

    def __init__(self, *, message=None, pointer=None, selected=None, hint=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the question text; a cool blue by default
        self.message = message if message is not None else hsl(210, 0.85, 0.62)
        # the highlighted option in a list; a calm cyan by default
        self.selected = selected if selected is not None else hsl(190, 0.75, 0.55)
        # the marker beside the highlight, matching the selection unless overridden
        self.pointer = pointer if pointer is not None else self.selected
        # the bracketed default; left uncolored unless a color is supplied
        self.hint = hint


def hsl(h: float, s: float, l: float):
    """
    Build a {chroma} color from a hue in degrees and saturation/lightness in [0, 1]; hand back
    {None} when the color bindings are unavailable, e.g. during bootstrap
    """
    # without the color bindings there is no color
    if pyre.libpyre is None:
        return None
    # chroma's kernel wants the hue in radians
    return pyre.libpyre.chroma.rgb.hsl(math.radians(h), s, l)


# the theme prompts fall back to when they are handed none
_default = None


def default() -> "Theme":
    """
    The current fallback theme, built on first use
    """
    # reach for the shared fallback
    global _default
    # make one lazily so importing the module costs nothing
    if _default is None:
        # build the default palette on first use
        _default = Theme()
    # hand it back
    return _default


def setDefault(theme: "Theme") -> None:
    """
    Install {theme} as the fallback every prompt uses
    """
    # replace the shared fallback
    global _default
    # install the caller's palette
    _default = theme
    # nothing to hand back
    return


# end of file
