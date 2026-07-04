# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the color helpers
from . import chroma


class Theme:
    """
    The palette a prompt paints with: the message, the pointer, the current choice, the hint
    """

    def __init__(self, *, message=None, pointer=None, selected=None, hint=None, **kwds):
        super().__init__(**kwds)
        # the question text; a cool blue by default
        self.message = message if message is not None else chroma.hsl(210, 0.85, 0.62)
        # the highlighted option in a list; a calm cyan by default
        self.selected = (
            selected if selected is not None else chroma.hsl(190, 0.75, 0.55)
        )
        # the marker beside the highlight, matching the selection unless overridden
        self.pointer = pointer if pointer is not None else self.selected
        # the bracketed default; left unstyled unless a color is supplied
        self.hint = hint


# the theme prompts fall back to when they are handed none
_default = None


def default() -> "Theme":
    """
    The current fallback theme, built on first use
    """
    global _default
    # make one lazily so importing the module costs nothing
    if _default is None:
        _default = Theme()
    return _default


def setDefault(theme: "Theme") -> None:
    """
    Install {theme} as the fallback every prompt uses
    """
    global _default
    _default = theme
    return


# end of file
