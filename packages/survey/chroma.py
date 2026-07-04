# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Truecolor helpers for styling prompts
"""


# externals
import os


# the SGR sequence that closes any active styling
RESET = "\x1b[0m"


def rgb(r: int, g: int, b: int) -> str:
    """
    The SGR foreground code for a 24-bit color
    """
    return f"\x1b[38;2;{r};{g};{b}m"


def hsl(h: float, s: float, l: float) -> str:
    """
    The SGR foreground code for a color given as hue in degrees and saturation/lightness in [0, 1]
    """
    return rgb(*_toRGB(h, s, l))


def paint(text: str, code: str, *, enabled: bool = True) -> str:
    """
    Wrap {text} in {code}, or hand it back untouched when styling is off or {code} is empty
    """
    # nothing to do when color is suppressed or there is no code to apply
    if not enabled or not code:
        return text
    # otherwise open with the code and close with a reset
    return f"{code}{text}{RESET}"


def enabled() -> bool:
    """
    Whether styling is permitted at all; honors the {NO_COLOR} convention
    """
    # a user who sets {NO_COLOR} wants none of it, regardless of the terminal
    return os.environ.get("NO_COLOR") is None


def _toRGB(h: float, s: float, l: float):
    """
    Convert an hsl color to an (r, g, b) triple of 0-255 integers
    """
    # the chroma of the color, and where the hue sits in the six 60-degree sectors
    c = (1 - abs(2 * l - 1)) * s
    hp = (h % 360) / 60
    # the second-largest component, and the base offset that sets the lightness
    x = c * (1 - abs(hp % 2 - 1))
    m = l - c / 2
    # pick the component ordering for the sector the hue falls in
    if hp < 1:
        r, g, b = c, x, 0
    elif hp < 2:
        r, g, b = x, c, 0
    elif hp < 3:
        r, g, b = 0, c, x
    elif hp < 4:
        r, g, b = 0, x, c
    elif hp < 5:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    # lift each component by the base and scale to a byte
    return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)


# end of file
