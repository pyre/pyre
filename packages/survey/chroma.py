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
    # assemble the truecolor foreground sequence
    return f"\x1b[38;2;{r};{g};{b}m"


def hsl(h: float, s: float, l: float) -> str:
    """
    The SGR foreground code for a color given as hue in degrees and saturation/lightness in [0, 1]
    """
    # convert to rgb, then build the sequence from the resulting channels
    return rgb(*_toRGB(h, s, l))


def paint(text: str, code: str, *, enabled: bool = True) -> str:
    """
    Wrap {text} in {code}, or hand it back untouched when styling is off or {code} is empty
    """
    # nothing to do when color is suppressed or there is no code to apply
    if not enabled or not code:
        # so hand the text back plain
        return text
    # otherwise wrap it so the styling stops where the text ends
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
    # how far the color departs from gray at this lightness
    c = (1 - abs(2 * l - 1)) * s
    # which of the six hue sectors it lands in
    hp = (h % 360) / 60
    # the ramp toward the neighboring primary
    x = c * (1 - abs(hp % 2 - 1))
    # the shift that lifts everything to the requested lightness
    m = l - c / 2
    # place the primaries by the sector the hue falls in, then lift to lightness below
    if hp < 1:
        # red full, green climbing toward yellow
        r, g, b = c, x, 0
    elif hp < 2:
        # green full, red receding from yellow
        r, g, b = x, c, 0
    elif hp < 3:
        # green full, blue climbing toward cyan
        r, g, b = 0, c, x
    elif hp < 4:
        # blue full, green receding from cyan
        r, g, b = 0, x, c
    elif hp < 5:
        # blue full, red climbing toward magenta
        r, g, b = x, 0, c
    else:
        # red full, blue receding from magenta
        r, g, b = c, 0, x
    # settle each channel at the requested lightness and express it as a byte
    return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)


# end of file
