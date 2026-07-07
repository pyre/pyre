# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
survey is a small toolkit for interactive terminal prompts
"""

# the prompt types
from .Prompt import Prompt
from .Input import Input
from .Confirm import Confirm
from .Select import Select

# the terminal and the key decoder, for building prompts of your own
from .Console import Console
from . import keys

# color: the palette type, the color builder, and the package-wide default
from .Theme import Theme
from .Theme import hsl
from .Theme import setDefault as set_theme


def text(*, message, default=None, **kwds) -> str:
    """
    Ask for a line of text and return it
    """
    # build an input prompt and ask it in one step
    return Input(message=message, default=default, **kwds).ask()


def confirm(*, message, default=True, **kwds) -> bool:
    """
    Ask a yes/no question and return a bool
    """
    # build a confirm prompt and ask it in one step
    return Confirm(message=message, default=default, **kwds).ask()


def select(*, message, options, default=None, **kwds) -> str:
    """
    Offer a list of options and return the one the user chooses
    """
    # build a select prompt and ask it in one step
    return Select(message=message, options=options, default=default, **kwds).ask()


# end of file
